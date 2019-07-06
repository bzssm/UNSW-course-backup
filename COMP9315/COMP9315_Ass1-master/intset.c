#include "postgres.h"
#include "fmgr.h"

PG_MODULE_MAGIC;

typedef struct Intset
{
	char[4]	v1_len;
	char[1]	data;
	int cdn; //cardinality?
} Intset;

Intset *parse_set(char *str) {
  int *arr = (int*)malloc(strlen(str)*sizeof(int));
  int j = 0, temp = 0, isNeg = 0;
  int numFound = 0;
  for(int i = 1; i < strlen(str); i++) {
    if (str[i] == ' ') {
      if (numFound == 1) {
        numFound = 2;
      } 
      continue;
    } else if (str[i] == ',' || str[i] == '}') {
      if (numFound != 0) {
        numFound = 0;
        arr[j] = temp; 
        temp = 0;
        isNeg = 0;
        j++;
      } else {
        return NULL;
      }
    } else if (str[i] >= '0' && str[i] <= '9') {
      if (numFound == 0) {
        numFound = 1;
      } else if (numFound == 2) {
        return NULL;
      }
      if (!isNeg) {
        temp = 10*temp + (str[i] - '0');
      } else {
        temp = 10*temp - (str[i] - '0');
      }
    } else if (str[i] == '-') {
      isNeg = 1;
    } 
  }
  Intset *s = (Intset *)palloc(sizeof(Intset));
  SET_VARSIZE(s,j);
  memcpy(s->data,arr,j);
  return s;
}

/*****************************************************************************
 * Input/Output functions
 *****************************************************************************/

PG_FUNCTION_INFO_V1(intset_in);

Datum
intset_in(PG_FUNCTION_ARGS)
{
	char *str = PG_GETARG_CSTRING(0);
	Intset *res = parse_set(str);
	if (res == NULL)
		ereport(ERROR,
				(errcode(ERRCODE_INVALID_TEXT_REPRESENTATION),
				 errmsg("invalid input syntax for int set: \"%s\"",
						str)));
	PG_RETURN_POINTER(result);
}

PG_FUNCTION_INFO_V1(intset_out);

Datum
intset_out(PG_FUNCTION_ARGS)
{
	Intset *s = (Intset *) PG_GETARG_POINTER(0);
	char	   *result;
	int len = VARSIZE(s);
	int *arr; 
	memcpy(arr,s->data,len - VARHDRSZ)
	
	result = psprintf("(%g,%g)", complex->x, complex->y);
	PG_RETURN_CSTRING(result);
}

/*****************************************************************************
 * Operators
 *****************************************************************************/

static bool
intset_con_internal(int i, Intset * a)
{
    int *arr;
    int len = VARSIZE(a);
    memcpy(arr, a->data, len - VARHDRSZ);
    
    for (j = 0; j < len; j++) {
        if (arr[j] == i) {
            return true;
        }
    }
    return false;
}

static bool
intset_sub_internal(Intset * a, Intset * b)
{
    int *arr;
    int len = VARSIZE(a);
    memcpy(arr, a->data, len - VARHDRSZ);
    
    for (i = 0; i < len; i++) {
        if (!(intset_con_internal(arr[i], b))) {
            return false;
        } else {
            continue;
        }
    }
    return true;
}

PG_FUNCTION_INFO_V1(intset_con);

Datum
intset_con(PG_FUNCTION_ARGS)
{
    int *i = (int *) PG_GETARG_POINTER(0);
    Intset *a = (Intset *) PG_GETARG_POINTER(1);
    
    PG_RETURN_BOOL(intset_con_internal(*i, a));
}

PG_FUNCTION_INFO_V1(intset_cdn);

Datum
intset_cdn(PG_FUNCTION_ARGS)
{
    Intset *a = (Intset *) PG_GETARG_POINTER(0);
    int len = VARSIZE(a);
    
    PG_RETURN_INT32(len);
}

PG_FUNCTION_INFO_V1(intset_sub);

Datum
intset_sub(PG_FUNCTION_ARGS)
{
    Intset *a = (Intset *) PG_GETARG_POINTER(0);
    Intset *b = (Intset *) PG_GETARG_POINTER(1);
    
    PG_RETURN_BOOL(intset_sub_internal(a, b));
}

PG_FUNCTION_INFO_V1(intset_eq);

Datum
intset_eq(PG_FUNCTION_ARGS)
{
    Intset *a = (Intset *) PG_GETARG_POINTER(0);
    Intset *b = (Intset *) PG_GETARG_POINTER(1);
    
    PG_RETURN_BOOL(intset_sub_internal(a, b) && intset_sub_internal(b, a));
}

PG_FUNCTION_INFO_V1(intset_int);

Datum
intset_int(PG_FUNCTION_ARGS)
{
    Intset *a = (Intset *) PG_GETARG_POINTER(0);
    Intset *b = (Intset *) PG_GETARG_POINTER(1);
    Intset *newset;
    
    int *a_arr;
    int a_len = VARSIZE(a);
    int b_len = VARSIZE(b);
    memcpy(a_arr, a->data, a_len - VARHDRSZ);
    
    max_size = (a_len <= b_len) ? a_len : b_len;
    int temp = malloc(max_size * sizeof(int));
    int step = 0;
    for (int i = 0; i < a_len; i++) {
        if (intset_con_internal(a_arr[i], b)) {
            temp[step] = a_arr[i];
            step = step + 1;
        }
    }
    
    newset = (Intset *) palloc(sizeof(Intset));
    memcpy(newset->data, temp, max_size * sizeof(int));
    PG_RETURN_POINTER(newset);
}

PG_FUNCTION_INFO_V1(intset_uni);

Datum
intset_uni(PG_FUNCTION_ARGS)
{
    Intset *a = (Intset *) PG_GETARG_POINTER(0);
    Intset *b = (Intset *) PG_GETARG_POINTER(1);
    Intset *newset;
    
    int *a_arr;
    int *b_arr;
    int a_len = VARSIZE(a);
    int b_len = VARSIZE(b);
    memcpy(a_arr, a->data, a_len - VARHDRSZ);
    memcpy(a_arr, a->data, a_len - VARHDRSZ);
    max_size = a_len + b_len;
    int temp = malloc(max_size * sizeof(int));
    int step = 0;
    for (int i = 0; i < a_len; i++) {
        temp[step] = a_arr[i];
        step = step + 1;
    }
    for (int j = 0; j < b_len; j++) {
        temp[step] = b_arr[j];
        step = step + 1;
    }
    
    newset = (Intset *) palloc(sizeof(Intset));
    memcpy(newset->data, temp, max_size * sizeof(int));
    PG_RETURN_POINTER(newset);
}

PG_FUNCTION_INFO_V1(intset_dis);

Datum
intset_dis(PG_FUNCTION_ARGS)
{
    Intset *a = (Intset *) PG_GETARG_POINTER(0);
    Intset *b = (Intset *) PG_GETARG_POINTER(1);
    Intset *newset;
    
    int *a_arr;
    int *b_arr;
    int a_len = VARSIZE(a);
    int b_len = VARSIZE(b);
    memcpy(a_arr, a->data, a_len - VARHDRSZ);
    memcpy(b_arr, b->data, b_len - VARHDRSZ);
    
    max_size = a_len + b_len;
    int temp = malloc(max_size * sizeof(int));
    int step = 0;
    for (int i = 0; i < a_len; i++) {
        if (!(intset_con_internal(a_arr[i], b))) {
            temp[step] = a_arr[i];
            step = step + 1;
        }
    }
    for (int j = 0; j < b_len; j++) {
        if (!(intset_con_internal(b_arr[i], a))) {
            temp[step] = b_arr[j];
            step = step + 1;
        }
    }
    
    newset = (Intset *) palloc(sizeof(Intset));
    memcpy(newset->data, temp, max_size * sizeof(int));
    PG_RETURN_POINTER(newset);
}

PG_FUNCTION_INFO_V1(intset_dif);

Datum
intset_dif(PG_FUNCTION_ARGS)
{
    Intset *a = (Intset *) PG_GETARG_POINTER(0);
    Intset *b = (Intset *) PG_GETARG_POINTER(1);
    Intset *newset;
    
    int *a_arr;
    int a_len = VARSIZE(a);
    int b_len = VARSIZE(b);
    memcpy(a_arr, a->data, a_len - VARHDRSZ);
    
    max_size = a_len;
    int temp = malloc(max_size * sizeof(int));
    int step = 0;
    for (int i = 0; i < a_len; i++) {
        if (!(intset_con_internal(a_arr[i], b))) {
            temp[step] = a_arr[i];
            step = step + 1;
        }
    }
    
    newset = (Intset *) palloc(sizeof(Intset));
    memcpy(newset->data, temp, max_size * sizeof(int));
    PG_RETURN_POINTER(newset);
}
