import sys

try:
    level = int(input('Enter a nonnegative integer: '))
    if level < 1:
        raise ValueError
except ValueError:
    sys.exit()

l = [[1],[1,1]]
for i in range(level-1):
    l.append([1])
    for i in range(len(l[len(l)-3])):
        l[len(l)-1].append(l[len(l)-2][i]+l[len(l)-2][i+1])
    l[len(l)-1].append(1)
print(l)