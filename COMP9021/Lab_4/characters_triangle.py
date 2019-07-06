import sys


def numberToLetter(num):
    return chr(64 + num)


def transformList(l):
    for i in range(len(l)):
        l[i] = chr(64 + l[i])
    # print(l)
    return (''.join(l))


def copyReverse(l):
    k = list(l)
    for i in range(2, len(l) + 1):
        l.append(k[-i])
    return l


try:
    level = int(input('Enter strictly positive number: '))
    if level <= 0:
        raise ValueError
except ValueError:
    sys.exit()

listOfLetter = [i for i in range(1, 27)] * (((1 + level) * level // 2) // 26 + 1)
listOfLetter = listOfLetter[:((1 + level) * level // 2) + 1]
listOfLetter.reverse()
rl = [[] for _ in range(level)]
print(listOfLetter)
for i in range(level):
    for j in range(i + 1):
        rl[i].append(listOfLetter.pop())
for l in rl:
    l = copyReverse(l)
for i in rl:
    spaceNum = level - 1 - len(i) // 2
    spaceList = [' '] * spaceNum
    kk = transformList(i)
    print(''.join(spaceList), end='')
    print(kk)
    # print(''.join(spaceList))
    # # print(''.join(i))
    # print((''.join(str([' ']*(2*level-1-len(i)))))+i+(''.join(str([' ']*(2*level-1-len(i))))))
# print(rl)
