
#include <string.h>
#include <stdlib.h>
#include <ctype.h>


//typedef struct intSet {
//    int *nums;
//    int length;
//} intSet;
//
//int main() {
//
//    typedef struct intSet {
//        int length;
//        char v1_len[4];
//        char *data;
//    } intSet;
//
//    char *input = "{1,2,3}";
//    char *pch;
//    int capacity = 1;
//    int length = 0;
//    int *x;
//
//    char *str;
//    str = (char *) malloc((strlen(input) - 2) * sizeof(char) + 1);
//    strncpy(str, input + sizeof(char), strlen(input) - 2);
//    str[strlen(input) - 2] = '\0';
//
//    x = (int *) malloc(capacity * sizeof(int));
//    pch = strtok(str, ",");
//    int i = 0, j = 0;
//    while (pch != NULL) {
//        int pchlen = strlen(pch);
//        int isnum = 0, temp = 0, isneg = 0, curnum = 0, repeat = 0, stop = 0,
//                terminal = 0;
//
//        for (j = 0; j < pchlen; j++) {
//            if (pch[j] == ' ' && isnum == 0) {
//                continue;
//            }
//            if (pch[j] == '-' && isnum == 0) {
//                isnum = 1;
//                isneg = 1;
//                continue;
//            }
//            if (pch[j] >= '0' && pch[j] <= '9' && isnum == 0 && stop == 0) {
//                isnum = 1;
//                temp = pch[j] - '0';
//                continue;
//            }
//            if (pch[j] >= '0' && pch[j] <= '9' && isnum == 1 && stop == 0) {
//                curnum = pch[j] - '0';
//                temp = temp * 10 + curnum;
//                continue;
//            }
//            if (pch[j] == ' ' && isnum == 1) {
//                stop = 1;
//                continue;
//            }
//
//            terminal = 1;
//            break;
//        }
//        if (terminal != 0) {
//            printf("123");
//            break;
//        }
//
//        if (isneg == 1) {
//            temp *= -1;
//        }
//
//        if (i != 0) {
//            for (j = 0; j < length; j++) {
//                if (x[j] == temp) {
//                    repeat = 1;
//                    break;
//                }
//            }
//        }
//        if (repeat == 1) {
//            pch = strtok(NULL, ",");
//            continue;
//        }
//        x[i] = temp;
//        i++;
//
//        // array length extend
//        if (i == capacity) {
//            capacity *= 2;
//            x = (int *) realloc(x, capacity * sizeof(int));
//        }
//        pch = strtok(NULL, ",");
//
//        // get real length
//        length = i;
//    }
//    intSet *intset = (intSet *) malloc(sizeof(intSet));
//    intset->data = (char *) realloc(intset->data,length*sizeof(int));
//    memcpy(intset->data, x, length);
//    printf("%s",intset->data);
/*
char input[] = "{1, {2,3}, 4}";
char *pch;
int arraylength = 1;
int length = 0;
int *x;
intSet *res;
int repeat = 0;
int isnum = 1;

char *str;
str = (char *) malloc((strlen(input) - 2) * sizeof(char) + 1);
strncpy(str, input + sizeof(char), strlen(input)-2);
str[strlen(input)-2]='\0';
printf("\n%s", str);

x = (int *) malloc(arraylength * sizeof(int));
pch = strtok(str, " ,");
int i = 0;
while (pch != NULL) {
    // check num
    int len = strlen(pch);
    for (int j = 0; j < len; j++) {
        if (!(isdigit(pch[j]))&& pch[j]!='-') {
            isnum = 0;
            break;
        }
    }
    if (isnum == 0) {
        isnum = 1;
        pch = strtok(NULL, " ,");
        continue;
    }

    // check repeat
    if (i != 0) {
        for (int j = 0; j < length; j++) {
            if (x[j] == atoi(pch)) {
                repeat = 1;
                break;
            }
        }
    }

    // if repeat, jump
    if (repeat == 1) {
        repeat = 0;
        pch = strtok(NULL, " ,");
        continue;
    }

    // if not repeat, add to array
    x[i] = atoi(pch);
    i++;

    // array length extend
    if (i == arraylength) {
        arraylength *= 2;
        x = (int *) realloc(x, arraylength * sizeof(int));
    }
    pch = strtok(NULL, " ,");

    // get real length
    length = i;
}
for (i = 0; i < length; i++)
    printf("\n%d", x[i]);
printf("\n\n%d", arraylength);
return 0;
 */




/*
char *result;
int nums[] = {1,2,3,4,5};
int length = 5;
char s[100];

result = (char *)malloc(length*sizeof(int)+length+2);
result[0]='{';
for(int i=0;i<length;i++){
    sprintf(s,"%d",nums[i]);
    strcat(result,s);
    if (i!=length-1)
        strcat(result,",");
}
strcat(result,"}");
strcat(result,"\0");
printf("%s",result);
 */

//}
//typedef struct intSet {
//    int length;
//    int capacity;
//    int *arraydata;
//} intSet;
//
//intSet *string_to_set(char *input){
//    char *str;
//    str = (char *)malloc((strlen(input) - 2) * sizeof(char) + 1);
//    strncpy(str, input + sizeof(char), strlen(input) - 2);
//    str[strlen(input) - 2] = '\0';
//
//    int *x;
//    int length = 0;
//    int capacity = 1;
//    char *pch;
//    x = (int *)malloc(capacity * sizeof(int));
//    pch = strtok(str, ",");
//    int i = 0, j = 0;
//    while (pch != NULL) {
//        int pchlen = strlen(pch);
//        int isnum = 0, temp = 0, isneg = 0, curnum = 0, repeat = 0, stop = 0,
//                terminal = 0;
//
//        for (j = 0; j < pchlen; j++) {
//            if (pch[j] == ' ' && isnum == 0) {
//                continue;
//            }
//            if (pch[j] == '-' && isnum == 0) {
//                isnum = 1;
//                isneg = 1;
//                continue;
//            }
//            if (pch[j] >= '0' && pch[j] <= '9' && isnum == 0 && stop == 0) {
//                isnum = 1;
//                temp = pch[j] - '0';
//                continue;
//            }
//            if (pch[j] >= '0' && pch[j] <= '9' && isnum == 1 && stop == 0) {
//                curnum = pch[j] - '0';
//                temp = temp * 10 + curnum;
//                continue;
//            }
//            if (pch[j] == ' ' && isnum == 1) {
//                stop = 1;
//                continue;
//            }
//
//            terminal = 1;
//            break;
//        }
//        if (terminal != 0) {
//            printf("???");
//            break;
//        }
//
//        if (isneg == 1) {
//            temp *= -1;
//        }
//
//        if (i != 0) {
//            for (j = 0; j < length; j++) {
//                if (x[j] == temp) {
//                    repeat = 1;
//                    break;
//                }
//            }
//        }
//        if (repeat == 1) {
//            pch = strtok(NULL, ",");
//            continue;
//        }
//        x[i] = temp;
//        i++;
//
//        // array length extend
//        if (i == capacity) {
//            capacity *= 2;
//            x = (int *)realloc(x, capacity * sizeof(int));
//        }
//        pch = strtok(NULL, ",");
//
//        // get real length
//        length = i;
//    }
//
//    intSet *res = (intSet *) malloc(sizeof(intSet));
//    res->length = length;
//    res->capacity = capacity;
//    res->arraydata = x;
//
//    return res;
//}
//
//char *set_to_string(int *array,int length){
//    char s[100];
//
//    char *result = (char *)malloc(length * 20 + length + 2);
//    result[0] = '{';
//    int i = 0;
//    for (i = 0; i < length; i++) {
//        sprintf(s, "%d", array[i]);
//        strcat(result, s);
//        if (i != length - 1) strcat(result, ",");
//    }
//    strcat(result, "}");
//    strcat(result, "\0");
//    result = (char *) realloc(result, strlen(result));
//    printf("%d",strlen(result));
//    printf("%d",sizeof(result));
//    printf("%s",result);
//    return result;
//}
//
//void swap(int *s, int i, int j) {
//    int temp;
//    temp = s[i];
//    s[i] = s[j];
//    s[j] = temp;
//}
//void quicksort(int *array, int n) {
//    if (n > 1) {
//        int pivot = 0, j;
//        for (j = 1; j < n; j++)
//            if (array[j] < array[0])
//                swap(array, ++pivot, j);
//        swap(array, 0, pivot);
//        quicksort(array, pivot);
//        quicksort(array + pivot + 1, n - pivot - 1);
//    }
void readTuple(FILE *in)
{
    printf("%s",in);

}

int main() {
    char *q = "WTF??";
    readTuple(q);
    int i = ceil(1/2);
    printf("%d",i);

}










