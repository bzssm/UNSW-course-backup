from Assignment.Assignment_1_Question_2 import *
from itertools import permutations

all = permutations('12345678',8)
allList = list()
for i in all:
    allList.append(int(''.join(list(i))))
print(allList)
all_dic = dict()
count=0
for i in allList:
    all_dic[i] = bfs(12345678,i)
    count+=1
    print(count)