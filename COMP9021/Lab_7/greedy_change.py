import sys
from collections import defaultdict

try:
    total = int(input('Input the desired amount: '))
except Exception:
    print('wrong!')
    sys.exit()
print()
noteList=[100,50,20,10,5,2,1]
result = defaultdict(int)
sum1=0
for e in noteList:
    while sum1<total:
        if sum1+e>total:
            break
        else:
            sum1+=e
            result[e]+=1
totalnum = sum([result[e] for e in result.keys()])
if totalnum==1:
    print('1 banknote is needed.')
else:
    print(f'{totalnum} banknotes are needed')
for e in sorted(result.items(),key = lambda x:x[0],reverse=True):
    print(('$'+str(e[0])).rjust(4)+':',result[e[0]])