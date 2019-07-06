# Randomly fills a grid of size height and width whose values are input by the user,
# with nonnegative integers randomly generated up to an upper bound N also input the user,
# and computes, for each n <= N, the number of paths consisting of all integers from 1 up to n
# that cannot be extended to n+1.
# Outputs the number of such paths, when at least one exists.
#
# Written by *** and Eric Martin for COMP9021


import sys
from collections import defaultdict
from random import seed, randint


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))


def get_paths():
    result = defaultdict(int)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                for e in dfs(grid, (i, j)):
                    result[e] += 1
    return result


def subnodes(grid, x, y):
    subnode = []
    if x - 1 >= 0:
        subnode.append((x - 1, y))
    if x + 1 < len(grid):
        subnode.append((x + 1, y))
    if y - 1 >= 0:
        subnode.append((x, y - 1))
    if y + 1 < len(grid[0]):
        subnode.append((x, y + 1))

    validSubnodes = [(i, j) for (i, j) in subnode if grid[i][j] == grid[x][y] + 1]
    return validSubnodes


def dfs(grid, startNode):
    # usedNode = set()
    queue = list()
    queue.append(startNode)
    result = []
    while len(queue) > 0:
        node = queue.pop()
        if len(subnodes(grid, node[0], node[1])) == 0:
            result.append(grid[node[0]][node[1]])
        for n in subnodes(grid, node[0], node[1]):
            queue.append(n)
    return result


# Insert your code for other functions

try:
    for_seed, max_length, height, width = [int(i) for i in
                                           input('Enter four nonnegative integers: ').split()
                                           ]
    if for_seed < 0 or max_length < 0 or height < 0 or width < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[randint(0, max_length) for _ in range(width)] for _ in range(height)]
print('Here is the grid that has been generated:')
display_grid()
paths = get_paths()
if paths:
    for length in sorted(paths):
        print(f'The number of paths from 1 to {length} is: {paths[length]}')
        print('The number of paths from 1 to ',length,' is: ',paths[length])
