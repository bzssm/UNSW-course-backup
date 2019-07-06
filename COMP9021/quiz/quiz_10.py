# Randomly generates N distinct integers with N provided by the user,
# inserts all these elements into a priority queue, and outputs a list
# L consisting of all those N integers, determined in such a way that:
# - inserting the members of L from those of smallest index of those of
#   largest index results in the same priority queue;
# - L is preferred in the sense that the last element inserted is as large as
#   possible, and then the penultimate element inserted is as large as possible, etc.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, sample

from copy import deepcopy

from quiz.priority_queue_adt import *

def preferred_sequence():
    result = []
    pqcopy = deepcopy(pq)
    while len(L):
        for e in sorted(L,reverse=True):
            beforepq = deepcopy(pqcopy)
            pqcopy._data[pqcopy._data.index(e)]=-1
            pqcopy._bubble_down(pqcopy._data.index(-1))
            pqcopy._data[pqcopy._data.index(-1)] = None
            pqcopy._length-=1
            possiblepq = deepcopy(pqcopy)
            pqcopy.insert(e)
            if pqcopy._data==beforepq._data:
                result.append(e)
                L.pop(L.index(e))
                pqcopy = deepcopy(possiblepq)
                break
            else:
                pqcopy = deepcopy(beforepq)
    return list(reversed(result))


try:
    for_seed, length = [int(x) for x in input('Enter 2 nonnegative integers, the second one '
                                                                             'no greater than 100: '
                                             ).split()
                       ]
    if for_seed < 0 or length > 100:
        raise ValueError
except ValueError:
    print('Incorrect input (not all integers), giving up.')
    sys.exit()    
seed(for_seed)
L = sample(list(range(length * 10)), length)
pq = PriorityQueue()
for e in L:
    pq.insert(e)
print('The heap that has been generated is: ')
print(pq._data[ : len(pq) + 1])
print('The preferred ordering of data to generate this heap by successsive insertion is:')
print(preferred_sequence())

