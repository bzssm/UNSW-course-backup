# Written by *** and Eric Martin for COMP9021


'''
Generates a list L of random nonnegative integers, the largest possible value
and the length of L being input by the user, and generates:
- a list "fractions" of strings of the form 'a/b' such that:
    . a <= b;
    . a*n and b*n both occur in L for some n
    . a/b is in reduced form
  enumerated from smallest fraction to largest fraction
  (0 and 1 are exceptions, being represented as such rather than as 0/1 and 1/1);
- if "fractions" contains then 1/2, then the fact that 1/2 belongs to "fractions";
- otherwise, the member "closest_1" of "fractions" that is closest to 1/2,
  if that member is unique;
- otherwise, the two members "closest_1" and "closest_2" of "fractions" that are closest to 1/2,
  in their natural order.
'''

import sys
from random import seed, randint
from math import gcd
import time


try:
    arg_for_seed, length, max_value = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, length, max_value = int(arg_for_seed), int(length), int(max_value)
    if arg_for_seed < 0 or length < 0 or max_value < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(0, max_value) for _ in range(length)]
if not any(e for e in L):
    print('\nI failed to generate one strictly positive number, giving up.')
    sys.exit()
print('\nThe generated list is:')
print('  ', L)

fractions = []
spot_on, closest_1, closest_2 = [None] * 3

# Replace this comment with your code
from fractions import Fraction as Frac

fractions_set = set()
for i in range(len(L)):
    for j in range(len(L)):
        if L[j] != 0 and Frac(L[i], L[j]) <= 1:
            fractions_set.add(Frac(L[i], L[j]))

# for e in fractions_set:
    # print(type(e))
starttime=time.time()
fractions = sorted(list(fractions_set))
print(time.time()-starttime)
# print(fractions)
for fraction in fractions:
    if fraction == Frac(1, 2):
        spot_on = True
        break
fraction_to_half_distance = dict()
for fraction in fractions:
    fraction_to_half_distance.setdefault(fraction, abs(fraction - Frac(1, 2)))
min_distance = 1
for fraction in fraction_to_half_distance:
    if fraction_to_half_distance[fraction] < min_distance:
        min_distance = fraction_to_half_distance[fraction]
# print(min_distance)
if min_distance != 0:
    count = 0
    min_distance_list = []
    for fraction in fraction_to_half_distance:
        if fraction_to_half_distance[fraction] == min_distance:
            min_distance_list.append(fraction)
            count += 1
    if count == 1:
        closest_1 = min_distance_list[0]
    elif count == 2:
        closest_1 = min_distance_list[0]
        closest_2 = min_distance_list[1]
else:
    spot_on = True

# print(fraction_to_half_distance)
for i in range(len(fractions)):
    fractions[i] = str(fractions[i])


print('\nThe fractions no greater than 1 that can be built from L, from smallest to largest, are:')
print('  ', '  '.join(e for e in fractions))
if spot_on:
    print('One of these fractions is 1/2')
elif closest_2 is None:
    print('The fraction closest to 1/2 is', closest_1)
else:
    print(closest_1, 'and', closest_2, 'are both closest to 1/2')
