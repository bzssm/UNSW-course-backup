from random import seed, randint
import sys
import statistics
import math


def my_mean(list):
    sum = 0.0
    for e in list:
        sum += e
    return sum / len(list)


def my_median(list):
    list.sort()
    if len(list) % 2 == 0:
        return (list[len(list) // 2] + list[len(list) // 2 - 1]) / 2
    else:
        return list[int(len(list) // 2) + 1]


def my_standard_deviation(list):
    standard_deviation = 0.0
    for i in range(len(list)):
        standard_deviation += ((list[i] - my_mean(list)) ** 2)
    return math.sqrt(standard_deviation / len(list))


arg_for_seed = input('Input a seed for the random number generator: ')
try:
    arg_for_seed = int(arg_for_seed)
except ValueError:
    print('Input is not an integer, giving up.')
    sys.exit()
nb_of_elements = input('How many elements do you want to generate? ')
try:
    nb_of_elements = int(nb_of_elements)
except ValueError:
    print('Input is not an integer, giving up.')
    sys.exit()
if nb_of_elements <= 0:
    print('Input should be strictly positive, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(-50, 50) for _ in range(nb_of_elements)]
print('\nThe list is:', L)
print()

print(f'The mean is {my_mean(L)}')
print(f'The median is {my_median(L)}')
print(f'The standard deviation is {my_standard_deviation(L)}')
print()
print('Confirming with functions from the statistics module:')
print(f'The mean is {statistics.mean(L)}')
print(f'The median is {statistics.median(L)}')
print(f'The standard deviation is {statistics.pstdev(L)}')
