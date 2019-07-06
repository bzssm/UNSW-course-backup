// tsig.h ... interface to functions on tuple signatures
// part of SIMC signature files
// Written by John Shepherd, September 2018

#ifndef TSIG_H
#define TSIG_H 1

#include "defs.h"
#include "query.h"
#include "reln.h"
#include "bits.h"

Bits makeAttributeSig(char *, int, int);
Bits makeTupleSig(Reln, Tuple);
Bits makeTupleSigWithMK(Reln, Tuple, int, int);
void findPagesUsingTupSigs(Query);

#endif
