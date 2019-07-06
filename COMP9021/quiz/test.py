from quiz.priority_queue_adt import *
from random import sample


pq = PriorityQueue(4)
L=[2,26,48,16,24]
for e in L:
    pq.insert(e)
print(pq._data)
pq._data[2]=0
pq._bubble_down(2)
print(pq._data)
print(sample(list(range(10)),11))