from itertools import product, compress


def encode(num):
    fibonacciList = [0,1]
    while (fibonacciList[len(fibonacciList) - 1] < num):
        fibonacciList.append(fibonacciList[len(fibonacciList) - 1] + fibonacciList[len(fibonacciList) - 2])
    length=0
    print(fibonacciList)
    for e in fibonacciList:
        if num>e:
            length+=1
    length-=1
    print(length)
    for e in list(product('01',repeat=length)):
        if decode(''.join(list(e)))==num:
            print(''.join(list(e)))
            e=list(e)
            e.reverse()
            print(e)


def decode(string):
    fibonacciList = [0, 1]
    while (len(fibonacciList)<len(string)+2):
        fibonacciList.append(fibonacciList[len(fibonacciList) - 1] + fibonacciList[len(fibonacciList) - 2])
    return sum(list(compress(fibonacciList[2:],map(int,string))))