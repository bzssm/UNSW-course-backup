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
from random import seed, randrange

from quiz.stack_adt import *


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))


directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
next_directions = {' ': ('W', 'S', 'E', 'N'),
                   'N': ('W', 'E', 'N'),
                   'S': ('E', 'W', 'S'),
                   'E': ('N', 'S', 'E'),
                   'W': ('S', 'N', 'W')}


def n_steps(node, previous_direction, path):
    x, y = node[0], node[1]
    result = []
    for next_direction in next_directions[previous_direction]:
        next_x, next_y = x + directions[next_direction][0], \
                         y + directions[next_direction][1],
        if next_x not in range(10) or next_y not in range(10):
            continue
        if (next_x, next_y) in path:
            continue
        result.append((next_x, next_y, next_direction))
    return result


def explore_depth_first(x, y, target):
    queue = Stack()
    queue.push([(x, y), ' '])
    sumnow = grid[x][y]
    while len(queue):
        node = queue.pop()
        path = node[:len(node) - 1]
        direction = node[-1]
        sumnow = sum(grid[e[0]][e[1]] for e in path)
        if sumnow == target:
            return path
        if sumnow > target:
            continue
        nextsteps = n_steps(path[-1], direction, path)
        nextpaths = []
        for e in nextsteps:
            if (e[0], e[1]) not in path:
                pathbackup = list(path)
                path.append((e[0], e[1]))
                path.append(e[2])
                nextpaths.append(path)
                path = list(pathbackup)
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
