//#include <stdio.h>
//#include <stdlib.h>
//
//typedef struct _BitsRep {
//    unsigned int nbits;        // how many bits
//    unsigned int nbytes;// how many bytes in array
//    unsigned char a;
//    unsigned char b;
//    unsigned char bitstring[1];  // array of bytes to hold bits
//
//} BitsRep;
//
//typedef struct _BitsRep *Bits;
//
//Bits newBits(int nbits) {
//    unsigned int nbytes = nbits/8;
//    Bits new = malloc(2 * sizeof(unsigned int) + nbytes);
//    new->nbits = nbits;
//    new->nbytes = nbytes;
//    new->a = "1";
//    new->b = "2";
//    memset(&(new->bitstring[0]), 0, nbytes);
//    return new;
//}
//
//int main() {
//    Bits new = newBits(64);
//    printf("%d\n",sizeof(unsigned int));
//    printf("%d\n", new);
//    printf("%d\n", &new->nbits);
//    printf("%d\n", &new->nbytes);
//    printf("%d\n", &new->a);
//    printf("%d\n", &new->b);
//    printf("%d\n", &new->bitstring);
//
//    return 0;
//}

#include <stdio.h>
#include <string.h>

struct student
{
    unsigned int id1;
    unsigned int id2;
    unsigned char a;
    unsigned char b;
    unsigned char bitstring[1];
};

int main()
{
    int i;
    struct student record1 = {1, 2, 'A', 'B', 90.5};

    printf("size of structure in bytes : %d\n",
           sizeof(record1));

    printf("\nAddress of id1        = %d", &record1.id1 );
    printf("\nAddress of id2        = %d", &record1.id2 );
    printf("\nAddress of a          = %d", &record1.a );
    printf("\nAddress of b          = %d", &record1.b );
    printf("\nAddress of percentage = %d",&record1.bitstring);

    return 0;
}