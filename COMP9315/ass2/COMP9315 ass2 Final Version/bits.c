// bits.c ... functions on bit-strings
// part of SIMC signature files
// Bit-strings are arbitrarily long byte arrays
// Least significant bits (LSB) are in array[0]
// Most significant bits (MSB) are in array[nbytes-1]

// Written by John Shepherd, September 2018

#include <assert.h>
#include "defs.h"
#include "bits.h"
#include "page.h"

typedef struct _BitsRep {
    Count nbits;        // how many bits
    Count nbytes;       // how many bytes in array
    Byte bitstring[1];  // array of bytes to hold bits
                        // actual array size is nbytes
} BitsRep;

// create a new Bits object

Bits newBits(int nbits) {
    Count nbytes = iceil(nbits, 8);
    Bits new = malloc(2 * sizeof(Count) + nbytes);
    new->nbits = nbits;
    new->nbytes = nbytes;
    memset(&(new->bitstring[0]), 0, nbytes);
    return new;
}

// release memory associated with a Bits object

void freeBits(Bits b) {
    // TODO FINISH
    free(b);
    b = NULL;
}

// check if the bit at position is 1

Bool bitIsSet(Bits b, int position) {
    assert(b != NULL);
    assert(0 <= position && position < b->nbits);
    // TODO FINISH
    int checkbyte = position / 8;
    int checkbit = position % 8;

    Byte mask = (1 << checkbit);
    Byte *currentbitstring = malloc(b->nbytes);

    memcpy(currentbitstring, &(b->bitstring), b->nbytes);

    if (currentbitstring[checkbyte] & mask) {
        free(currentbitstring);
        return TRUE;
    } else {
        free(currentbitstring);
        return FALSE;
    }

    
}

// check whether one Bits b1 is a subset of Bits b2

Bool isSubset(Bits b1, Bits b2) {
    assert(b1 != NULL && b2 != NULL);
    assert(b1->nbytes == b2->nbytes);
    // printf("!!!!!!");
    // //below for test
    // printf("Bit1:");
    // for (int i = 0; i < b1->nbits; i++) {
    //     if (bitIsSet(b1,i)) {
    //         printf("%d, ",i);
    //     }
    // }
    // printf("\n");
    // printf("Bit2:");
    // for (int i = 0; i < b2->nbits; i++) {
    //     if (bitIsSet(b2,i)) {
    //         printf("%d, ",i);
    //     }
    // }
    // printf("\n");
    // TODO FINISH
    for (int i = 0; i < b1->nbytes; i++) {
        if ((b1->bitstring[i] & b2->bitstring[i]) != b1->bitstring[i]) {
            return FALSE;
        }
    }

    return TRUE;
}

// set the bit at position to 1

void setBit(Bits b, int position) {
    assert(b != NULL);
    assert(0 <= position && position < b->nbits);
    // TODO FINISH
    int changebyte = position / 8;
    int changebit = position % 8;

    Byte mask = (1 << changebit);
    Byte *currentbitstring = malloc(b->nbytes);

    memcpy(currentbitstring, &(b->bitstring), b->nbytes);
    currentbitstring[changebyte] = currentbitstring[changebyte] | mask;
    memcpy(&(b->bitstring), currentbitstring, b->nbytes);

    free(currentbitstring);
}

// set all bits to 1

void setAllBits(Bits b) {
    assert(b != NULL);
    // TODO FINISH
    int changebyte = b->nbytes;
    int changebit = b->nbits % 8;
    Byte all1mask = 255;
    Byte remainmask = (1 << changebit) - 1;
    Byte *currentbitstring = malloc(b->nbytes);

    memcpy(currentbitstring, &(b->bitstring), b->nbytes);
    for (int i = changebyte - 2; i >= 0; i--) {
        currentbitstring[i] = currentbitstring[i] | all1mask;
    }
    currentbitstring[changebyte - 1] =
        currentbitstring[changebyte - 1] | remainmask;
    memcpy(&(b->bitstring), currentbitstring, b->nbytes);

    free(currentbitstring);
}

// set the bit at position to 0

void unsetBit(Bits b, int position) {
    assert(b != NULL);
    assert(0 <= position && position < b->nbits);
    // TODO FINISH
    int changebyte = position / 8;
    int changebit = position % 8;

    Byte mask = ~(1 << changebit);
    Byte *currentbitstring = malloc(b->nbytes);

    memcpy(currentbitstring, &(b->bitstring), b->nbytes);
    currentbitstring[changebyte] = currentbitstring[changebyte] & mask;
    memcpy(&(b->bitstring), currentbitstring, b->nbytes);

    free(currentbitstring);
}

// set all bits to 0

void unsetAllBits(Bits b) {
    assert(b != NULL);
    // TODO FINISH
    int changebyte = b->nbytes;
    Byte all1mask = 0;
    Byte *currentbitstring = malloc(b->nbytes);

    memcpy(currentbitstring, &(b->bitstring), b->nbytes);
    for (int i = changebyte - 1; i >= 0; i--) {
        currentbitstring[i] = currentbitstring[i] & all1mask;
    }
    memcpy(&(b->bitstring), currentbitstring, b->nbytes);

    free(currentbitstring);
}

// bitwise AND ... b1 = b1 & b2

void andBits(Bits b1, Bits b2) {
    assert(b1 != NULL && b2 != NULL);
    assert(b1->nbytes == b2->nbytes);
    // TODO FINISH
    int changebyte = b1->nbytes;
    Byte *currentbitstring = calloc(1, b1->nbytes);

    memcpy(currentbitstring, &(b1->bitstring), b1->nbytes);
    for (int i = changebyte - 1; i >= 0; i--) {
        currentbitstring[i] = b1->bitstring[i] & b2->bitstring[i];
    }
    memcpy(&(b1->bitstring), currentbitstring, b1->nbytes);

    free(currentbitstring);
}

// bitwise OR ... b1 = b1 | b2

void orBits(Bits b1, Bits b2) {
    assert(b1 != NULL && b2 != NULL);
    assert(b1->nbytes == b2->nbytes);
    // TODO FINISH
    int changebyte = b1->nbytes;
    Byte *currentbitstring = calloc(1, b1->nbytes);

    memcpy(currentbitstring, &(b1->bitstring), b1->nbytes);
    for (int i = changebyte - 1; i >= 0; i--) {
        currentbitstring[i] = b1->bitstring[i] | b2->bitstring[i];
    }
    memcpy(&(b1->bitstring), currentbitstring, b1->nbytes);

    free(currentbitstring);
}

// get a bit-string (of length b->nbytes)
// from specified position in Page buffer
// and place it in a BitsRep structure

void getBits(Page p, Offset pos, Bits b) {
    // TODO FINISH
    memcpy(
        &(b->bitstring[0]),
        addrInPage(p, pos, b->nbytes),
        b->nbytes);
}

// copy the bit-string array in a BitsRep
// structure to specified position in Page buffer

void putBits(Page p, Offset pos, Bits b) {
    // TODO FINISH
    memcpy(
        addrInPage(p, pos, b->nbytes),
        &(b->bitstring[0]), 
        b->nbytes);
}

// show Bits on stdout
// display in order MSB to LSB
// do not append '\n'

void showBits(Bits b) {
    assert(b != NULL);
    // printf("(%d,%d)", b->nbits, b->nbytes);
    for (int i = b->nbytes - 1; i >= 0; i--) {
        for (int j = 7; j >= 0; j--) {
            Byte mask = (1 << j);
            if (b->bitstring[i] & mask)
                putchar('1');
            else
                putchar('0');
        }
    }
}

unsigned int nbit(Bits b){
	return b->nbits;
}

unsigned int nbyte(Bits b){
    return b->nbytes;
}