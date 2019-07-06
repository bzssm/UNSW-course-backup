def int_to_set(n):
    result_set=set()
    for e in str(n):
        result_set.add(e)
    return result_set

result_list=list()
for i in range(10,100):
    for j in range(i,100):
        for k in range(j,100):
            if int_to_set(i)|int_to_set(j)|int_to_set(k) == int_to_set(i*j*k) and len(int_to_set(i*j*k))==6:
                result_list.append((i,j,k))
# print(result_list)
for i in result_list:
    a,b,c=i
    print(f'{a} x {b} x {c} = {a*b*c}')