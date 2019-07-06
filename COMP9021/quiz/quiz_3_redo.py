# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and finds out, for given step_number >= 1
# and step_size >= 2, the number of stairs of step_number many steps,
# with all steps of size step_size.
#
# A stair of 1 step of size 2 is of the form
# 1 1
#   1 1
#
# A stair of 2 steps of size 2 is of the form
# 1 1
#   1 1
#     1 1
#
# A stair of 1 step of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#
# A stair of 2 steps of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#         1
#         1 1 1
#
# The output lists the number of stairs from smallest step sizes to largest step sizes,
# and for a given step size, from stairs with the smallest number of steps to stairs
# with the largest number of stairs.
#
# Written by *** and Eric Martin for COMP9021


import sys
from collections import defaultdict
from random import seed, randint


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))


        # Replace return {} above with your code


# Possibly define other functions
def generate_list(dim, size):
    result_list = list()
    result_list += ['right'] * (size - 1)
    while len(result_list) < 2 * dim:
        result_list += ['down'] * (size - 1)
        result_list += ['right'] * (size - 1)
        result_list += ['step']
    return result_list


def check_stairs(direction_list, grid, i, j):
    step = 0
    for e in direction_list:
        if e == 'right':
            j += 1
        elif e == 'down':
            i += 1
        elif e == 'step':
            step += 1
        if i == len(grid) or j == len(grid):
            break
        if grid[i][j] != 0:
            continue
        else:
            break
    return step


def stairs_in_grid():
    dic = defaultdict(lambda: defaultdict(int))
    for k in (2, (len(grid) + 1) // 2 + 1):  # size
        for i in range(0, len(grid) - k + 1):
            for j in range(0, len(grid) - 2 * k + 2):
                dic[k][check_stairs(generate_list(len(grid),k),grid,i,j)]+=1
    reduce_repeat(dic)
    return dic

def reduce_repeat(dic):
    for i in dic:
        for j in sorted(dic[i]):
            dic[i][j]-=dic[i][j+1]
try:
    arg_for_seed, density, dim = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density, dim = int(arg_for_seed), int(density), int(dim)
    if arg_for_seed < 0 or density < 0 or dim < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
# A dictionary whose keys are step sizes, and whose values are pairs of the form
# (number_of_steps, number_of_stairs_with_that_number_of_steps_of_that_step_size),
# ordered from smallest to largest number_of_steps.
stairs = stairs_in_grid()
for step_size in sorted(stairs):
    print(f'\nFor steps of size {step_size}, we have:')
    for nb_of_steps in stairs[step_size]:
        stair_or_stairs = 'stair' if stairs[step_size][nb_of_steps] == 1 else 'stairs'
        step_or_steps = 'step' if nb_of_steps == 1 else 'steps'
        print(f'     {stairs[step_size][nb_of_steps]} {stair_or_stairs} with {nb_of_steps} {step_or_steps}')
