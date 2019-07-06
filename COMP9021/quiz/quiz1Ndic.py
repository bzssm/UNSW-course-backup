L=[1,4,4,1,2,4,3]
N=[]
cp=0
d={}
for i in range(len(L)):
    d[i]=0
i=0
while(7!= sum(d[i] for i in range (len(L)))):
    if d[cp]!=1:
        N+=[L[cp]]
        d[cp] = 1
        cp=L[cp]

    else:
        for i in range(len(L)):
            if d[i]==0:
                cp=i
                break
        N+=[L[cp]]
        d[cp] = 1
        cp=L[cp]

print(N)