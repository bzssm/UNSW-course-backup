#include "postgres.h"

#include "fmgr.h"

PG_MODULE_MAGIC;

typedef struct intSet {
    char vl_len_[4];
    char data[1];
    int length;
} intSet;

PG_FUNCTION_INFO_V1(intset_in);

Datum intset_in(PG_FUNCTION_ARGS) {
    char *input = PG_GETARG_CSTRING(0);
    char *pch;
    int capacity = 1;
    int length = 0;
    int *x;

    char *str;
    str = (char *)malloc((strlen(input) - 2) * sizeof(char) + 1);
    strncpy(str, input + sizeof(char), strlen(input) - 2);
    str[strlen(input) - 2] = '\0';

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
    intSet *intset = (intSet *)palloc(sizeof(intSet));
    SET_VARSIZE(intset, length);
    memcpy(intset->data, x, length);
    memcpy(intset.length, length, sizeof(int));
    PG_RETURN_POINTER(intset);
}

PG_FUNCTION_INFO_V1(intset_out);

Datum intset_out(PG_FUNCTION_ARGS) {
    intSet *intset = (intSet *)PG_GETARG_POINTER(0);
    char *result;
    int *nums = intset->data;
    int length = intset->length;
    char s[100];

    result = (char *)malloc(length * sizeof(int) + length + 2);
    result[0] = '{';
    int i = 0;
    for (i = 0; i < length; i++) {
        sprintf(s, "%d", nums[i]);
        strcat(result, s);
        if (i != length - 1) strcat(result, ",");
    }
    strcat(result, "}");
    strcat(result, "\0");
    PG_RETURN_CSTRING(result);
}