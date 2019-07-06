import sys


def divisors(num):
    resultlist = []
    for i in range(1, num // 2 + 1):
        if num % i == 0:
            resultlist.append(i)
    return resultlist


number = input('Input an integer: ')
try:
    intnumber = int(number)
    if intnumber < 1:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

perfectnumberlist = []

for num in range(2, intnumber):
    sumnum = sum(i for i in divisors(num))
    if sumnum == num:
        perfectnumberlist.append(num)
    sumnum = 0
for i in perfectnumberlist:
    print(i, 'is a perfect number.')
