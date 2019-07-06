first = input('Please input the first string: ')
second = input('Please input the second string: ')
third = input('Please input the third string: ')
if len(first)==max(len(first),len(second),len(third)):
    mergedString = first
elif len(second)==max(len(first),len(second),len(third)):
    mergedString = second
elif len(third)==max(len(first),len(second),len(third)):
    mergedString = third
if len(first)+len(second)+len(third)!= len(mergedString)*2:
    print('No solution')
