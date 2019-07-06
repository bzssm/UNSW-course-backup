// psig.c ... functions on page signatures (psig's)
// part of SIMC signature files
// Written by John Shepherd, September 2018

#include <math.h>
#include "defs.h"
#include "reln.h"
#include "query.h"
#include "psig.h"
#include "tsig.h"
#include "tuple.h"

Bits makePageSig(Reln r, Tuple t) {
    assert(r != NULL && t != NULL);

    Page dataPage = getPage(r->dataf, nPages(r) - 1);
    Bits new = newBits(psigBits(r));

    Page currentPage = getPage(r->psigf, nPsigPages(r) - 1);
    if (pageNitems(dataPage) != 1) {
        getBits(currentPage, pageNitems(currentPage) - 1, new);
    }
    Tuple temp = malloc(tupSize(r));
    strcpy(temp, t);
    char *p;
    p = strtok(temp, ",");
    while (p != NULL) {
        orBits(new, makeAttributeSig(p, psigBits(r), codeBits(r)));
        p = strtok(NULL, ",");
    }

    return new;
}

void findPagesUsingPageSigs(Query q) {
    assert(q != NULL);
    // TODO FINISH
    Bits querytsig = makeTupleSigWithMK(q->rel, q->qstring, psigBits(q->rel),
                                        codeBits(q->rel));
    // showBits(querytsig);
    // printf("\n");

    for (int i = 0; i < nPsigPages(q->rel); i++) {
        // iter pages
        Page currentPage = getPage(psigFile(q->rel), i);

        q->nsigpages++;

        for (int j = 0; j < pageNitems(currentPage); j++) {
            // iter items in page
            Bits psig = newBits(psigBits(q->rel));
            getBits(currentPage, j, psig);
            q->nsigs++;
            // printf("@@@@@%d,%d", i*5+j, isSubset(querytsig, psig));
            if (isSubset(querytsig, psig)) {
                // match
                setBit(q->pages, i * maxPsigsPP(q->rel) + j);
            }
        }
    }
    // printf("Matched Pages:");
    // showBits(q->pages);
    // putchar('\n');
}
