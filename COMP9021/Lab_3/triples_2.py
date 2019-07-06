from math import sqrt


def find_square(n):
    result_list=list()
    for i in range(round(sqrt(n))):
        result_list.append(i**2)
    return result_list
def find_in_square_list(n,square_list):
    flag = False
    for i in range(len(square_list)):
        for j in range(i,len(square_list)):
            if n == i**2+j**2:
                flag = True

                return(flag, i, j)
    if flag == False:
        return(flag,None,None)




square_list = find_square(1000)

for k in range(100,998):
    a,b,c = find_in_square_list(k, square_list)
    d,e,f = find_in_square_list(k+1, square_list)
    g,h,i = find_in_square_list(k+2, square_list)
    if a==True and d==True and g==True:
        print(f'({k},{k+1},{k+2}) (equal to ({b}^2+{c}^2, {e}^2+{f}^2, {h}^2+{i}^2)) is a solution.')



