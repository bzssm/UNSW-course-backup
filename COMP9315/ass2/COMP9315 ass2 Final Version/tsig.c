// tsig.c ... functions on Tuple Signatures (tsig's)
// part of SIMC signature files
// Written by John Shepherd, September 2018

#include <unistd.h>
#include <string.h>
#include <math.h>
#include "defs.h"
#include "tsig.h"
#include "reln.h"
#include "hash.h"
#include "bits.h"
#include "tuple.h"
#include "page.h"

// make an attribute signature
// generate a bitstring with m length contains k 1s
// additional function
// written by Roy, 14 Oct 2018 19:00

Bits makeAttributeSig(char *attribute, int m, int k) {
    // TODO FINISH
    int nbits = 0;  // count of set bits
    // int m = tsigBits(r);
    // int k = codeBits(r);
    Bits new = newBits(m);

    // if an attribute is "?", return all 0 Bits.
    if (strcmp(attribute, "?") == 0) {
        return new;
    }

    // set a certain seed
    srandom(hash_any(attribute, strlen(attribute)));

    // make cw to an attribute
    while (nbits < k) {
        int i = random() % m;
        if (bitIsSet(new, i) == 0) {
            setBit(new, i);
            nbits++;
        }
    }
    return new;
}

// make a tuple signature

Bits makeTupleSig(Reln r, Tuple t) {
    assert(r != NULL && t != NULL);
    // TODO FINISH
    Bits new = newBits(tsigBits(r));
    char *p;


    Tuple temp = malloc(tupSize(r));
    strcpy(temp, t);
    p = strtok(temp, ",");


    while (p != NULL) {
        orBits(new, makeAttributeSig(p, tsigBits(r), codeBits(r)));
        p = strtok(NULL, ",");
    }
    
    return new;
}

Bits makeTupleSigWithMK(Reln r, Tuple t, int m, int k) {
    assert(r != NULL && t != NULL);
    // TODO FINISH
    Bits new = newBits(m);
    char *p;
    Tuple temp = malloc(tupSize(r));
    strcpy(temp, t);
    p = strtok(temp, ",");
    while (p != NULL) {
        orBits(new, makeAttributeSig(p, m, k));
        p = strtok(NULL, ",");
    }
    return new;
}

// find "matching" pages using tuple signatures

void findPagesUsingTupSigs(Query q) {
    assert(q != NULL);
    // TODO FINISH
    // char *<->FILE *???
    // Bits querytsig = makeTupleSig(q->rel, readTuple(q->rel, (FILE *)q->qstring));
    Bits querytsig = makeTupleSig(q->rel, q->qstring);
    // printf("%s", q->qstring);
    // showBits(querytsig);
    // printf("\n");

    for (int i = 0; i < nTsigPages(q->rel);i++) {
        // iter pages
        Page currentPage = getPage(tsigFile(q->rel), i);
        q->nsigpages++;

        for (int j = 0; j < pageNitems(currentPage); j++) {

            // iter items in page
            Bits tsig = newBits(tsigBits(q->rel));
            getBits(currentPage, j, tsig);
            q->nsigs++;
            
            if (isSubset(querytsig, tsig)) {
                // match

                int queryIndex = i * maxTsigsPP(q->rel) + j + 1;
                int queryPageId =
                    iceil(queryIndex , maxTupsPP(q->rel)) - 1;
                setBit(q->pages, queryPageId);

            }
        }
    }
    
    // The printf below is primarily for debugging
    // Remove it before submitting this function
    // printf("Matched Pages:");
    // showBits(q->pages);
    // putchar('\n');
}
