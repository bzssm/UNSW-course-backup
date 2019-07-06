// bsig.c ... functions on Tuple Signatures (bsig's)
// part of SIMC signature files
// Written by John Shepherd, September 2018

#include "defs.h"
#include "reln.h"
#include "query.h"
#include "bsig.h"
#include "tsig.h"

void findPagesUsingBitSlices(Query q) {
    assert(q != NULL);
    // TODO FINISH
    setAllBits(q->pages);
    // Bits checkBSPosition = newBits(bsigBits(q->rel));
    // setAllBits(checkBSPosition);
    Bits bsigPagesRecord = newBits(nBsigPages(q->rel));
    Bits querytsig = makeTupleSigWithMK(q->rel, q->qstring, psigBits(q->rel),
                                        codeBits(q->rel));
    for (int i = 0; i < psigBits(q->rel); i++) {
        if (bitIsSet(querytsig, i)) {
            Page bsPage =
                getPage(bsigFile(q->rel), iceil(i + 1, maxBsigsPP(q->rel)) - 1);
            // bsig read
            Bits bs = newBits(bsigBits(q->rel));
            q->nsigs++;

            // bsig pages read record
            if (!bitIsSet(bsigPagesRecord,
                          iceil(i + 1, maxBsigsPP(q->rel)) - 1)) {
                setBit(bsigPagesRecord, iceil(i + 1, maxBsigsPP(q->rel)) - 1);
            }
            getBits(bsPage, i % maxBsigsPP(q->rel), bs);
            for (int j = 0; j < nbit(q->pages); j++) {
                if (bitIsSet(q->pages, j)) {
                    if (!bitIsSet(bs, j)) {
                        unsetBit(q->pages, j);
                    }
                }
            }
            freeBits(bs);
        }
    }

    // count how many sig pages read
    for (int i = 0; i < nBsigPages(q->rel); i++) {
        if (bitIsSet(bsigPagesRecord, i)) {
            q->nsigpages++;
        }
    }

    freeBits(bsigPagesRecord);
    freeBits(querytsig);
}
