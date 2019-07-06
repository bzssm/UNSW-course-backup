#include "postgres.h"

#include "fmgr.h"

PG_MODULE_MAGIC;

typedef struct intSet {
    int length;
    int capacity;
    int *arraydata;
} intSet;

typedef struct store_struc {
    int32 length;
    char data[FLEXIBLE_ARRAY_MEMBER];
} store_struc;

intSet *string_to_set(char *input) {
    char *str;
    str = (char *)malloc((strlen(input) - 2) * sizeof(char) + 1);
    strncpy(str, input + sizeof(char), strlen(input) - 2);
    str[strlen(input) - 2] = '\0';

    int *x;
    int length = 0;
    int capacity = 1;
    char *pch;
    x = (int *)malloc(capacity * sizeof(int));
    pch = strtok(str, ",");
    int i = 0, j = 0;
    while (pch != NULL) {
        int pchlen = strlen(pch);
        int isnum = 0, temp = 0, isneg = 0, curnum = 0, repeat = 0, stop = 0,
            terminal = 0;

        for (j = 0; j < pchlen; j++) {
            if (pch[j] == ' ' && isnum == 0) {
                continue;
            }
            if (pch[j] == '-' && isnum == 0) {
                isnum = 1;
                isneg = 1;
                continue;
            }
            if (pch[j] >= '0' && pch[j] <= '9' && isnum == 0 && stop == 0) {
                isnum = 1;
                temp = pch[j] - '0';
                continue;
            }
            if (pch[j] >= '0' && pch[j] <= '9' && isnum == 1 && stop == 0) {
                curnum = pch[j] - '0';
                temp = temp * 10 + curnum;
                continue;
            }
            if (pch[j] == ' ' && isnum == 1) {
                stop = 1;
                continue;
            }

            terminal = 1;
            break;
        }
        if (terminal != 0) {
            ereport(ERROR, (errcode(ERRCODE_INVALID_TEXT_REPRESENTATION),
                            errmsg("invalid input syntax.\"%s\"", input)));
            break;
        }

        if (isneg == 1) {
            temp *= -1;
        }

        if (i != 0) {
            for (j = 0; j < length; j++) {
                if (x[j] == temp) {
                    repeat = 1;
                    break;
                }
            }
        }
        if (repeat == 1) {
            pch = strtok(NULL, ",");
            continue;
        }
        x[i] = temp;
        i++;

        // array length extend
        if (i == capacity) {
            capacity *= 2;
            x = (int *)realloc(x, capacity * sizeof(int));
        }
        pch = strtok(NULL, ",");

        // get real length
        length = i;
    }

    intSet *res = (intSet *)malloc(sizeof(intSet));
    res->length = length;
    res->capacity = capacity;
    res->arraydata = x;

    return res;
}

char *set_to_string(int *array, int length) {
    char s[100];

    char *result = (char *)malloc(length * 21 + 2);
    memset(result, 0, length * 21 + 2);

    result[0] = '{';
    int i = 0;
    for (i = 0; i < length; i++) {
        sprintf(s, "%d", array[i]);
        strcat(result, s);
        if (i != length - 1) strcat(result, ",");
    }
    strcat(result, "}");
    // strcat(result, '\0');
    return result;
}

PG_FUNCTION_INFO_V1(intset_in);

Datum intset_in(PG_FUNCTION_ARGS) {
    char *input = PG_GETARG_CSTRING(0);
    intSet *intset = string_to_set(input);
    int length = intset->length;
    int capacity = intset->capacity;
    int *data1 = intset->arraydata;

    char *string = set_to_string(data1, length);

    store_struc *dest = (store_struc *)palloc(VARHDRSZ + strlen(string));
    dest->length = (int32)strlen(string);
    SET_VARSIZE(dest, VARHDRSZ + strlen(string));
    memcpy(dest->data, string, strlen(string));
    PG_RETURN_POINTER(dest);
}

PG_FUNCTION_INFO_V1(intset_out);

Datum intset_out(PG_FUNCTION_ARGS) {
    store_struc *dest = (store_struc *)PG_GETARG_POINTER(0);
    char *res;
    res = (char *)palloc(100);
    snprintf(res, 100, "%s", dest->data);
    PG_RETURN_CSTRING(res);
}

int belong_core(int a,int *array, int length){
    int i=0;
    for(i=0;i<length;i++){
        if (array[i]==a){
            return 1;
        }
    }
    return 0;
}

intSet *intersetcion_core(int *arrayA,int *arrayB,int lengthA,int lengthB){
    int *res = (int *)malloc(sizeof(int)*lengthA);
    int length=0;
    int i=0;
    for (i=0;i<lengthA;i++){
        if (belong_core(arrayA[i],arrayB,lengthB)==1){
            res[length]==arrayA[i];
            length++;
        }
    }
    res = (int *)realloc(res,sizeof(int)*length);

    intSet *intset = (intSet *) malloc(sizeof(intSet));
    intset->arraydata = res;
    intset->length = length;
    intset->capacity = 1;
    return intset;
}

intSet *union_core(int *arrayA,int *arrayB,int lengthA,int lengthB){
    char *arraystringA = set_to_string(arrayA,lengthA);
    char *arraystringB = set_to_string(arrayB,lengthB);
    char *allstring = (char *)malloc(strlen(arraystringA)+strlen(arraystringB)-1);
    int i=0;
    
    char *strA = (char *)malloc((strlen(arraystringA) - 1) * sizeof(char) + 1);
    strncpy(strA, arraystringA, strlen(arraystringA) - 1);

    char *strB = (char *)malloc((strlen(arraystringB) - 1) * sizeof(char) + 1);
    strncpy(strB, arraystringB+sizeof(char), strlen(arraystringB) - 1);
    strB[strlen(arraystringB) - 1] = '\0';

    memcpy(allstring,strA,strlen(strA));
    memcpy(allstring+strlen(strA), strB, strlen(strB)+1);

    return string_to_set(allstring);
}

intSet *diff_core(int *arrayA,int *arrayB,int lengthA,int lengthB){
    int *res = (int *)malloc(sizeof(int)*lengthA);
    int length = 0;
    int i=0;
    for (i=0;i<lengthA;i++){
        if(belong_core(arrayA[i],arrayB,lengthB)==0){
            res[length]==arrayA[i];
            length++;
        }
    }

    res = (int *)realloc(res,sizeof(int)*length);

    intSet *intset = (intSet *) malloc(sizeof(intSet));
    intset->arraydata = res;
    intset->length = length;
    intset->capacity = 1;
    return intset;
}

PG_FUNCTION_INFO_V1(belong);

Datum belong(PG_FUNCTION_ARGS) {
    int i = (int *)PG_GETARG_POINTER(0);
    char *input = (char *)PG_GETARG_POINTER(1);
    intSet *intset = string_to_set(input);

    int res = belong_core(i, intset->arraydata, intset->length);
    PG_RETURN_BOOL(res==1);
}

PG_FUNCTION_INFO_V1(count);

Datum count(PG_FUNCTION_ARGS) {
    char *input = (char *)PG_GETARG_POINTER(0);
    intSet *intset = string_to_set(input);
    PG_RETURN_INT32(intset->length);
}

PG_FUNCTION_INFO_V1(subset);

Datum subset (PG_FUNCTION_ARGS){
    char *input1 = (char *)PG_GETARG_POINTER(0);
    char *input2 = (char *)PG_GETARG_POINTER(1);
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    int i=0;
    for (i=0;i<intsetA->length;i++){
        if (belong_core(intsetA->arraydata[i],intsetB->arraydata,intsetB->length)==0){
            PG_RETURN_BOOL(1==0);
        }
    }
    PG_RETURN_BOOL(1==1);
}

PG_FUNCTION_INFO_V1(equal);

Datum equal(PG_FUNCTION_ARGS){
    char *input1 = (char *)PG_GETARG_POINTER(0);
    char *input2 = (char *)PG_GETARG_POINTER(1);
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    int i=0;
    for (i=0;i<intsetA->length;i++){
        if(belong_core(intsetA->arraydata[i],intsetB->arraydata,intsetB->length)==0){
            PG_RETURN_BOOL(1==0);
        }
    }
    for(i=0;i<intsetB->length;i++){
        if(belong_core(intsetB->arraydata[i],intsetA->arraydata,intsetA->length)==0){
            PG_RETURN_BOOL(1==0);
        }
    }
    PG_RETURN_BOOL(1==1);
}

PG_FUNCTION_INFO_V1(intSet_intersection);

Datum intSet_intersection(PG_FUNCTION_ARGS){
    char *input1 = (char *)PG_GETARG_POINTER(0);
    char *input2 = (char *)PG_GETARG_POINTER(1);
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    intSet *res = intersetcion_core(intsetA->arraydata,intsetB->arraydata,intsetA->length,intsetB->length);

    char *string = set_to_string(res->arraydata, res->length);

    store_struc *dest = (store_struc *)palloc(VARHDRSZ + strlen(string));
    dest->length = (int32)strlen(string);
    SET_VARSIZE(dest, VARHDRSZ + strlen(string));
    memcpy(dest->data, string, strlen(string));
    PG_RETURN_POINTER(dest);
}

PG_FUNCTION_INFO_V1(intSet_union);

Datum intSet_union(PG_FUNCTION_ARGS){
    char *input1 = (char *)PG_GETARG_POINTER(0);
    char *input2 = (char *)PG_GETARG_POINTER(1);
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    intSet *res = union_core(intsetA->arraydata,intsetB->arraydata,intsetA->length,intsetB->length);
    char *string = set_to_string(res->arraydata, res->length);

    store_struc *dest = (store_struc *)palloc(VARHDRSZ + strlen(string));
    dest->length = (int32)strlen(string);
    SET_VARSIZE(dest, VARHDRSZ + strlen(string));
    memcpy(dest->data, string, strlen(string));
    PG_RETURN_POINTER(dest);
}

PG_FUNCTION_INFO_V1(intSet_disjunction);

Datum intSet_disjunction(PG_FUNCTION_ARGS){
    char *input1 = (char *)PG_GETARG_POINTER(0);
    char *input2 = (char *)PG_GETARG_POINTER(1);
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    intSet *A_B = diff_core(intsetA->arraydata,intsetB->arraydata,intsetA->length,intsetB->length);
    intSet *B_A = diff_core(intsetB->arraydata,intsetA->arraydata,intsetB->length,intsetA->length);
    intSet *res = union_core(A_B->arraydata,B_A->arraydata,A_B->length,B_A->length);
    char *string = set_to_string(res->arraydata, res->length);

    store_struc *dest = (store_struc *)palloc(VARHDRSZ + strlen(string));
    dest->length = (int32)strlen(string);
    SET_VARSIZE(dest, VARHDRSZ + strlen(string));
    memcpy(dest->data, string, strlen(string));
    PG_RETURN_POINTER(dest);

}

PG_FUNCTION_INFO_V1(intSet_diff);

Datum intSet_diff(PG_FUNCTION_ARGS){
    char *input1 = (char *)PG_GETARG_POINTER(0);
    char *input2 = (char *)PG_GETARG_POINTER(1);
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    intSet *res = diff_core(intsetA->arraydata,intsetB->arraydata,intsetA->length,intsetB->length);
    char *string = set_to_string(res->arraydata, res->length);

    store_struc *dest = (store_struc *)palloc(VARHDRSZ + strlen(string));
    dest->length = (int32)strlen(string);
    SET_VARSIZE(dest, VARHDRSZ + strlen(string));
    memcpy(dest->data, string, strlen(string));
    PG_RETURN_POINTER(dest);
}



