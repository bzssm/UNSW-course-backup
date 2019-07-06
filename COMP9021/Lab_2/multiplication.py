multiplier = []
for i in range(100, 1000):
    for j in range(10, 100):
        mul1 = (j % 10) * i
        mul2 = (j // 10) * i

        # sum1=(i%10)+(j%10)+(((j%10)*i)%10)+((i*j)%10)
        # sum2=int(str(i)[1])+int(str(j)[0])+int(str(j%)[1])
        if (len(str((j % 10) * i)) == 4) and (len(str((j // 10) * i)) == 3) and (len(str(i * j)) == 4):

            sum1 = int(str(i)[-1]) + int(str(j)[-1]) + int(str(mul1)[-1]) + int(str(i * j)[-1])
            sum2 = int(str(i)[-2]) + int(str(j)[-2]) + int(str(mul1)[-2]) + int(str(mul2)[-1]) + int(str(i * j)[-2])
            sum3 = int(str(i)[-3]) + int(str(mul1)[-3]) + int(str(mul2)[-2]) + int(str(i * j)[-3])
            sum4 = int(str(mul1)[-4]) + int(str(mul2)[-3]) + int(str(i * j)[-4])

            if sum1 == sum2 == sum3 == sum4:
                multiplier.append((i, j, sum1))
# print(multiplier)
for i in multiplier:
    a, b, c = i
    print(f'{a} * {b} = {a*b}, all columns adding up to {c}.')
