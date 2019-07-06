# Written by *** and Eric Martin for COMP9021


'''
Generates a list L of random nonnegative integers smaller than the length of L,
whose value is input by the user, and outputs two lists:
- a list M consisting of L's middle element, followed by L's first element,
  followed by L's last element, followed by L's second element, followed by
  L's penultimate element...;
- a list N consisting of L[0], possibly followed by L[L[0]], possibly followed by
  L[L[L[0]]]..., for as long as L[L[0]], L[L[L[0]]]... are unused, and then,
  for the least i such that L[i] is unused, followed by L[i], possibly followed by
  L[L[i]], possibly followed by L[L[L[i]]]..., for as long as L[L[i]], L[L[L[i]]]...
  are unused, and then, for the least j such that L[j] is unused, followed by L[j],
  possibly followed by L[L[j]], possibly followed by L[L[L[j]]]..., for as long as
  L[L[j]], L[L[L[j]]]... are unused... until all members of L have been used up.
'''

import sys
from random import seed, randrange

try:
    arg_for_seed, length = input('Enter two nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, length = int(arg_for_seed), int(length)
    if arg_for_seed < 0 or length < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randrange(length) for _ in range(length)]
print('\nThe generated list L is:')
print('  ', L)
M = []
N = []
# Replace this comment with your code
if len(L)!=0:

    Lbackup = list(L)
    M.append(L[len(L) // 2])
    L.pop(len(L) // 2)
    for _ in range(len(L) // 2):
        M.append(L.pop(0))
        M.append(L.pop(len(L) - 1))
    if len(L) != 0:
        M.append(L.pop(0))

    # print(Lbackup)
    L = list(Lbackup)
    # print(L)
    current_location = 0
    record = ['not used'] * len(L)
    for _ in range(len(L)):
        if record[current_location] != 'used':
            N.append(L[current_location])
            record[current_location] = 'used'
            current_location = L[current_location]
        # else:
        #     for i in range(current_location,len(L)):
        #         test=False
        #         if record[i]!='used':
        #             N.append(L[i])
        #             record[i]='used'
        #             current_location=i
        #             test=True
        #     if test== False:
        #         for i in range(0,current_location):
        #             test = False
        #             if record[i] != 'used':
        #                 N.append(L[i])
        #                 record[i] = 'used'
        #                 current_location = i
        #                 test = True

        else:
            for i in range(len(L)):

                if record[i] != 'used':
                    N.append(L[i])
                    record[i] = 'used'
                    current_location = L[i]
                    break
else:
    print('Incorrect input, giving up.')
    sys.exit()

print('\nHere is M:')
print('  ', M)
print('\nHere is N:')
print('  ', N)
print('\nHere is L again:')
print('  ', L)
