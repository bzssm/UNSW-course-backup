import sys


def fill_list(number):
    # find N(how many whole group:
    n = 0
    while True:
        # Sn = 4 * n ** 2 + 2 * n
        if 4 * n ** 2 + 2 * n <= number:
            n += 1
        else:
            break

    # print(n)
    list_of_directions = list()
    # 1 more group

    list_of_directions += ['None']
    for i in range(n):
        list_of_directions += ['right'] * (2 * i + 1)
        list_of_directions += ['down'] * (2 * i + 1)
        list_of_directions += ['left'] * (2 * i + 2)
        list_of_directions += ['up'] * (2 * i + 2)
    print('123123')
    return list_of_directions


def turn_right(l):
    temp = l[5]
    l[5] = l[0]
    l[0] = l[4]
    l[4] = l[1]
    l[1] = temp


def turn_down(l):
    temp = l[5]
    l[5] = l[2]
    l[2] = l[4]
    l[4] = l[3]
    l[3] = temp
    return


def turn_left(l):
    temp = l[5]
    l[5] = l[1]
    l[1] = l[4]
    l[4] = l[0]
    l[0] = temp


def turn_up(l):
    temp = l[5]
    l[5] = l[3]
    l[3] = l[4]
    l[4] = l[2]
    l[2] = temp


goal_cell_number_input = input('Enter the desired goal cell number: ')
while True:
    try:
        goal_cell_number = int(goal_cell_number_input)
        if goal_cell_number <= 0:
            raise ValueError
        break
    except ValueError:
        print('Incorrect value, try again')
        goal_cell_number_input = input('Enter the desired goal cell number: ')

direction_list = fill_list(goal_cell_number)
# print(direction_list)
# List seq: right left front back top bot
number_list = [1, 6, 2, 5, 3, 4]
j = 0
while (((6 * j) + 1) ** 2) <= goal_cell_number:
    j += 1
j -= 1
print(j)

if goal_cell_number == 1:
    print(
        f'On cell {goal_cell_number}, {number_list[4]} is at the top, {number_list[2]} at the front, and {number_list[0]} on the right.')
else:
    for i in range((((6 * j) + 1) ** 2), goal_cell_number):
        if direction_list[i] == 'right':
            turn_right(number_list)
        elif direction_list[i] == 'left':
            turn_left(number_list)
        elif direction_list[i] == 'up':
            turn_up(number_list)
        elif direction_list[i] == 'down':
            turn_down(number_list)
    print(
        f'On cell {goal_cell_number}, {number_list[4]} is at the top, {number_list[2]} at the front, and {number_list[0]} on the right.')
