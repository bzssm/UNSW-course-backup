// psig.c ... functions on page signatures (psig's)
// part of SIMC signature files
// Written by John Shepherd, September 2018

#include "defs.h"
#include "reln.h"
#include "query.h"
#include "psig.h"
#include "tsig.h"
#include "tuple.h"

Bits makePageSig(Reln r, Tuple t) {
    assert(r != NULL && t != NULL);
    // TODO FINISH? NO TEST
    Bits new = newBits(psigBits(r));
    int id = nPages(r) - 1;
    Page currentPage = getPage(dataFile(r), id);
    for (int i = 0; i < pageNitems(currentPage); i++) {
        Tuple t = getTupleFromPage(r, currentPage, i);
        char *p;
        p = strtok(t, ",");
        while (p != NULL) {
            orBits(new, makeAttributeSig(p, psigBits(r), codeBits(r)));
            p = strtok(NULL, ",");
        }
    }
    return new;
}

void findPagesUsingPageSigs(Query q)
{
	assert(q != NULL);
	//TODO
	setAllBits(q->pages); // remove this
}

