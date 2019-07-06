from itertools import combinations

digits = int(input("Input a number that we will use as available digits: "))
desiredSum = int(input("Input a number that represents the desired sum: "))
count=0
wishList=[]
for i in range(1,len(str(digits))+1):
    possibleNumbers = list(combinations(str(digits),i))
    for e in possibleNumbers:

        sumnow = sum(map(int,e))

        if sumnow == desiredSum:
            wishList.append(e)

if len(wishList)>1:
    print(f'There are {len(wishList)} solutions.')
elif len(wishList)==1:
    print('There is a unique solution.')
else:
    print('There is no solution.')
