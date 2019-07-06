import sys

from math import factorial


def div(num):
    res = 0
    for _ in range(len(str(num))):
        if num % 10 == 0:
            res += 1
            num = num // 10
        else:
            break
    return res


def conv(num):
    strnum = str(num)
    res = 0
    for i in range(1, len(strnum)):
        if strnum[-1 * i] == '0':
            res += 1
        else:
            break
    return res


# def smart(num):



number = input('Input a nonnegative integer at least equal to 5: ')
try:
    intnumber = int(number)
    if intnumber < 5:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
fac = factorial(intnumber)
print(fac)
print(div(fac))
print(conv(fac))
