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

void swap(int *s, int i, int j) {
    int temp;
    temp = s[i];
    s[i] = s[j];
    s[j] = temp;
}
void quicksort(int *array, int n) {
    if (n > 1) {
        int pivot = 0, j;
        for (j = 1; j < n; j++)
            if (array[j] < array[0]) swap(array, ++pivot, j);
        swap(array, 0, pivot);
        quicksort(array, pivot);
        quicksort(array + pivot + 1, n - pivot - 1);
    }
}

intSet *string_to_set(char *input) {
    char *str;
    str = (char *)malloc((strlen(input) - 2) * sizeof(char) + 1);
    memcpy(str, input + sizeof(char), strlen(input) - 2);
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
            if (pch[j] == '}') {
                break;
            }

            terminal = 1;
            break;
        }
        if (terminal != 0) {
            ereport(ERROR, (errcode(ERRCODE_INVALID_TEXT_REPRESENTATION),
                            errmsg("invalid input syntax:\"%s\"", input)));
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
        if (isnum == 1) {
            x[i] = temp;
            i++;
        }

        // array length extend
        if (i == capacity) {
            capacity *= 2;
            x = (int *)realloc(x, capacity * sizeof(int));
        }
        pch = strtok(NULL, ",");

        // get real length
        length = i;
    }

    if (length != 0) {
        quicksort(x, length);
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
    result = realloc(result, strlen(result) * sizeof(char));
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
    res = (char *)palloc(strlen(dest->data) + 1);
    snprintf(res, strlen(dest->data) + 1, "%s", dest->data);
    PG_RETURN_CSTRING(res);
}

int belong_core(int a, int *array, int length) {
    int i = 0;
    for (i = 0; i < length; i++) {
        if (array[i] == a) {
            return 1;
        }
    }
    return 0;
}

intSet *intersetcion_core(int *arrayA, int *arrayB, int lengthA, int lengthB) {
    int *res = (int *)malloc(sizeof(int) * lengthA);
    int length = 0;
    int i = 0;
    for (i = 0; i < lengthA; i++) {
        if (belong_core(arrayA[i], arrayB, lengthB) == 1) {
            res[length] = arrayA[i];
            length++;
        }
    }
    res = (int *)realloc(res, sizeof(int) * length);

    if (length != 0) {
        quicksort(res, length);
    }
    intSet *intset = (intSet *)malloc(sizeof(intSet));
    intset->arraydata = res;
    intset->length = length;
    intset->capacity = 1;
    return intset;
}

intSet *union_core(int *arrayA, int *arrayB, int lengthA, int lengthB) {
    intSet *intset = (intSet *)malloc(sizeof(intSet));
    int *res = (int *)malloc((lengthA + lengthB) * sizeof(int));
    int i = 0;
    int length = 0;
    for (i = 0; i < lengthA; i++) {
        if (belong_core(arrayA[i], res, length) == 0) {
            res[length] = arrayA[i];
            length++;
        }
    }
    for (i = 0; i < lengthB; i++) {
        if (belong_core(arrayB[i], res, length) == 0) {
            res[length] = arrayB[i];
            length++;
        }
    }

    if (length != 0) {
        quicksort(res, length);
    }

    intset->arraydata = res;
    intset->length = length;
    intset->capacity = 1;
    return intset;
}

intSet *diff_core(int *arrayA, int *arrayB, int lengthA, int lengthB) {
    int *res = (int *)malloc(sizeof(int) * lengthA);
    int length = 0;
    int i = 0;
    for (i = 0; i < lengthA; i++) {
        if (belong_core(arrayA[i], arrayB, lengthB) == 0) {
            res[length] = arrayA[i];
            length++;
        }
    }

    res = (int *)realloc(res, sizeof(int) * length);

    if (length != 0) {
        quicksort(res, length);
    }

    intSet *intset = (intSet *)malloc(sizeof(intSet));
    intset->arraydata = res;
    intset->length = length;
    intset->capacity = 1;
    return intset;
}

PG_FUNCTION_INFO_V1(belong);

Datum belong(PG_FUNCTION_ARGS) {
    int i = PG_GETARG_INT32(0);
    store_struc *rawinput = (store_struc *)PG_GETARG_POINTER(1);
    char *input = rawinput->data;
    intSet *intset = string_to_set(input);

    int res = belong_core(i, intset->arraydata, intset->length);
    PG_RETURN_BOOL(res == 1);
}

PG_FUNCTION_INFO_V1(count);

Datum count(PG_FUNCTION_ARGS) {
    store_struc *rawinput = (store_struc *)PG_GETARG_POINTER(0);
    char *input = rawinput->data;
    intSet *intset = string_to_set(input);
    PG_RETURN_INT32(intset->length);
}

PG_FUNCTION_INFO_V1(subset);

Datum subset(PG_FUNCTION_ARGS) {
    store_struc *rawinput1 = (store_struc *)PG_GETARG_POINTER(0);
    store_struc *rawinput2 = (store_struc *)PG_GETARG_POINTER(1);

    char *input1 = rawinput1->data;
    char *input2 = rawinput2->data;

    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    int i = 0;
    for (i = 0; i < intsetA->length; i++) {
        if (belong_core(intsetA->arraydata[i], intsetB->arraydata,
                        intsetB->length) == 0) {
            PG_RETURN_BOOL(1 == 0);
        }
    }
    PG_RETURN_BOOL(1 == 1);
}

PG_FUNCTION_INFO_V1(equal);

Datum equal(PG_FUNCTION_ARGS) {
    store_struc *rawinput1 = (store_struc *)PG_GETARG_POINTER(0);
    store_struc *rawinput2 = (store_struc *)PG_GETARG_POINTER(1);

    char *input1 = rawinput1->data;
    char *input2 = rawinput2->data;
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    int i = 0;
    for (i = 0; i < intsetA->length; i++) {
        if (belong_core(intsetA->arraydata[i], intsetB->arraydata,
                        intsetB->length) == 0) {
            PG_RETURN_BOOL(1 == 0);
        }
    }
    for (i = 0; i < intsetB->length; i++) {
        if (belong_core(intsetB->arraydata[i], intsetA->arraydata,
                        intsetA->length) == 0) {
            PG_RETURN_BOOL(1 == 0);
        }
    }
    PG_RETURN_BOOL(1 == 1);
}

PG_FUNCTION_INFO_V1(intset_intersection);

Datum intset_intersection(PG_FUNCTION_ARGS) {
    store_struc *rawinput1 = (store_struc *)PG_GETARG_POINTER(0);
    store_struc *rawinput2 = (store_struc *)PG_GETARG_POINTER(1);

    char *input1 = rawinput1->data;
    char *input2 = rawinput2->data;

    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    intSet *res = intersetcion_core(intsetA->arraydata, intsetB->arraydata,
                                    intsetA->length, intsetB->length);

    char *string = set_to_string(res->arraydata, res->length);

    store_struc *dest = (store_struc *)palloc(VARHDRSZ + strlen(string));
    dest->length = (int32)strlen(string);
    SET_VARSIZE(dest, VARHDRSZ + strlen(string));
    memcpy(dest->data, string, strlen(string));
    PG_RETURN_POINTER(dest);
}

PG_FUNCTION_INFO_V1(intset_union);

Datum intset_union(PG_FUNCTION_ARGS) {
    store_struc *rawinput1 = (store_struc *)PG_GETARG_POINTER(0);
    store_struc *rawinput2 = (store_struc *)PG_GETARG_POINTER(1);

    char *input1 = rawinput1->data;
    char *input2 = rawinput2->data;
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    intSet *res = union_core(intsetA->arraydata, intsetB->arraydata,
                             intsetA->length, intsetB->length);
    char *string = set_to_string(res->arraydata, res->length);

    store_struc *dest = (store_struc *)palloc(VARHDRSZ + strlen(string));
    dest->length = (int32)strlen(string);
    SET_VARSIZE(dest, VARHDRSZ + strlen(string));
    memcpy(dest->data, string, strlen(string));
    PG_RETURN_POINTER(dest);
}

PG_FUNCTION_INFO_V1(intset_disjunction);

Datum intset_disjunction(PG_FUNCTION_ARGS) {
    store_struc *rawinput1 = (store_struc *)PG_GETARG_POINTER(0);
    store_struc *rawinput2 = (store_struc *)PG_GETARG_POINTER(1);

    char *input1 = rawinput1->data;
    char *input2 = rawinput2->data;
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    intSet *A_B = diff_core(intsetA->arraydata, intsetB->arraydata,
                            intsetA->length, intsetB->length);
    intSet *B_A = diff_core(intsetB->arraydata, intsetA->arraydata,
                            intsetB->length, intsetA->length);
    intSet *res =
        union_core(A_B->arraydata, B_A->arraydata, A_B->length, B_A->length);
    char *string = set_to_string(res->arraydata, res->length);

    store_struc *dest = (store_struc *)palloc(VARHDRSZ + strlen(string));
    dest->length = (int32)strlen(string);
    SET_VARSIZE(dest, VARHDRSZ + strlen(string));
    memcpy(dest->data, string, strlen(string));
    PG_RETURN_POINTER(dest);
}

PG_FUNCTION_INFO_V1(intset_diff);

Datum intset_diff(PG_FUNCTION_ARGS) {
    store_struc *rawinput1 = (store_struc *)PG_GETARG_POINTER(0);
    store_struc *rawinput2 = (store_struc *)PG_GETARG_POINTER(1);

    char *input1 = rawinput1->data;
    char *input2 = rawinput2->data;
    intSet *intsetA = string_to_set(input1);
    intSet *intsetB = string_to_set(input2);

    intSet *res = diff_core(intsetA->arraydata, intsetB->arraydata,
                            intsetA->length, intsetB->length);
    char *string = set_to_string(res->arraydata, res->length);

    store_struc *dest = (store_struc *)palloc(VARHDRSZ + strlen(string));
    dest->length = (int32)strlen(string);
    SET_VARSIZE(dest, VARHDRSZ + strlen(string));
    memcpy(dest->data, string, strlen(string));
    PG_RETURN_POINTER(dest);
}
