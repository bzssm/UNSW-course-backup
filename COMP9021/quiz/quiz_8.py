# Randomly fills a grid of size 10 x 10 with digits between 0
# and bound - 1, with bound provided by the user.
# Given a point P of coordinates (x, y) and an integer "target"
# also all provided by the user, finds a path starting from P,
# moving either horizontally or vertically, in either direction,
# so that the numbers in the visited cells add up to "target".
# The grid is explored in a depth-first manner, first trying to move north,
# always trying to keep the current direction,
# and if that does not work turning in a clockwise manner.
#
# Written by Eric Martin for COMP9021


import sys
from copy import deepcopy
from random import seed, randrange

from quiz.stack_adt import *


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))


direction_order = {'original': ['W', 'S', 'E', 'N'],
                   'W': ['S', 'N', 'W'],
                   'S': ['E', 'W', 'S'],
                   'E': ['N', 'S', 'E'],
                   'N': ['W', 'E', 'N']}
usedpoint = set()


def subnodes(node):
    subnodeslist = []
    for e in direction_order[node[2]]:
        if e == 'W':
            x = node[0]
            y = node[1] - 1
        elif e == 'S':
            x = node[0] + 1
            y = node[1]
        elif e == 'E':
            x = node[0]
            y = node[1] + 1
        elif e == 'N':
            x = node[0] - 1
            y = node[1]
        subnodeslist.append((x, y, e))
    return [e for e in subnodeslist if
            e[0] in range(len(grid)) and e[1] in range(len(grid)) and (e[0], e[1]) not in usedpoint]


def getpath(queueoriginal):
    path = []
    queue = deepcopy(queueoriginal)
    for _ in range(len(queue)):
        temp = queue.pop().pop()
        path.append((temp[0], temp[1]))
    path.reverse()
    return path


def updatesum(queue):
    return sum(grid[e[0]][e[1]] for e in getpath(queue))


def backtrack(queue):
    while queue.peek() == []:
        queue.pop()
        if len(queue) == 0:
            queue = None
            break
        queue.peek().pop()



def explore_depth_first(x, y, target):
    queue = Stack()
    queue.push([(x, y, 'original')])
    sumnow = 0
    sumnow += grid[x][y]
    while sumnow < target and len(queue) != 0:
        node = queue.peek()[-1]
        usedpoint.add((node[0], node[1]))
        if subnodes(node) == []:
            queue.push(subnodes(node))
            backtrack(queue)
            sumnow = updatesum(queue)
            continue
        queue.push(subnodes(node))
        sumnow = updatesum(queue)
        if sumnow < target:
            continue
        elif sumnow > target:
            while sumnow > target:
                queue.peek().pop()
                if queue.peek() != []:
                    sumnow = updatesum(queue)
                else:
                    backtrack(queue)
                    sumnow = updatesum(queue)

                if sumnow == target:
                    return getpath(queue)
                while queue.peek() == []:
                    backtrack(queue)
                    sumnow = updatesum(queue)

        else:
            return getpath(queue)


try:
    for_seed, bound, x, y, target = [int(x) for x in input('Enter five integers: ').split()]
    if bound < 1 or x not in range(10) or y not in range(10) or target < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [[randrange(bound) for _ in range(10)] for _ in range(10)]

print('Here is the grid that has been generated:')
display_grid()
path = explore_depth_first(x, y, target)
if not path:
    print(f'There is no way to get a sum of {target} starting from ({x}, {y})')
else:
    print('With North as initial direction, and exploring the space clockwise,')
    print(f'the path yielding a sum of {target} starting from ({x}, {y}) is:')
    print(path)
