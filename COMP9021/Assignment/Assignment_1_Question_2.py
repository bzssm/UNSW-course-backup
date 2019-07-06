import sys
from collections import deque


def t1(seqint):
    seq = [e for e in str(seqint)]
    rseq = [0] * 8
    rseq[0], rseq[1], rseq[2], rseq[3], rseq[4], rseq[5], rseq[6], rseq[7] = seq[7], seq[6], seq[5], seq[4], seq[3], \
                                                                             seq[2], seq[1], seq[0]
    return int(''.join(rseq))


def t2(seqint):
    seq = [e for e in str(seqint)]
    rseq = [0] * 8
    rseq[0], rseq[1], rseq[2], rseq[3], rseq[4], rseq[5], rseq[6], rseq[7] = seq[3], seq[0], seq[1], seq[2], seq[5], \
                                                                             seq[6], seq[7], seq[4]
    return int(''.join(rseq))


def t3(seqint):
    seq = [e for e in str(seqint)]
    rseq = [0] * 8
    rseq[0], rseq[1], rseq[2], rseq[3], rseq[4], rseq[5], rseq[6], rseq[7] = seq[0], seq[6], seq[1], seq[3], seq[4], \
                                                                             seq[2], seq[5], seq[7]
    return int(''.join(rseq))


def subnodes(seq):
    return [t1(seq), t2(seq), t3(seq)]


def backtraceToCount(parent, startNode, soughtValue):
    path = [soughtValue]
    while path[-1] != startNode:
        path.append(parent[path[-1]])
    # path.reverse()
    # print(path)
    return len(path) - 1


def input_soughtValue():
    stringSoughtValue = input('Input final configuration: ')
    stringSoughtValue = stringSoughtValue.replace(' ', '')
    setSoughtValue = {c for c in stringSoughtValue}
    try:
        for c in stringSoughtValue:
            if not (int(c) >= 1 and int(c) <= 8 and len(stringSoughtValue) == 8 and len(setSoughtValue) == 8):
                raise ValueError
        soughtValue = int(stringSoughtValue)
    except ValueError:
        print('Incorrect configuration, giving up...')
        sys.exit()
    return soughtValue


def bfs(startNode, soughtValue):
    son_father = {}
    usedNode = set()
    queue = deque([startNode])
    queue_set = set(queue)
    while len(queue) > 0:
        node = queue.pop()
        queue_set.remove(node)
        if node in usedNode:
            continue
        usedNode.add(node)
        if node == soughtValue:
            return backtraceToCount(son_father, startNode, soughtValue)
        for n in subnodes(node):
            if n not in usedNode and n not in queue_set:
                queue.appendleft(n)
                queue_set.add(n)
                son_father[n] = node


originalStatus = 12345678
soughtValue = input_soughtValue()
# print(t1(originalStatus))
# print(bfs(originalStatus,15324678))
count = bfs(originalStatus,soughtValue)
if count==0 or count ==1:
    print(f'{count} step is needed to reach the final configuration.')
else:
    print(f'{count} steps are needed to reach the final configuration.')
