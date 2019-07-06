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


def subnodes(node,direction):
    subnodeslist = []
    for e in direction_order[direction]:
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
            e[0] in range(len(grid)) and e[1] in range(len(grid))]

def getsum(path):
    return sum(grid[e[0]][e[1]] for e in path)


def explore_depth_first(x, y, target):
    queue = Stack()
    queue.push([(x,y),'original'])
    sumnow = grid[x][y]
    while len(queue):
        node = queue.pop()
        path = node[:len(node)-1]
        direction = node[-1]
        sumnow = getsum(path)
        if sumnow==target:
            return path
        if sumnow>target:
            continue
        nextsteps=subnodes(path[-1],direction)
        nextpaths=[]
        for e in nextsteps:
            if (e[0],e[1]) not in path:
                pathbackup=list(path)
                path.append((e[0],e[1]))
                path.append(e[2])
                nextpaths.append(path)
                path=list(pathbackup)
        for e in nextpaths:
            queue.push(e)





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
