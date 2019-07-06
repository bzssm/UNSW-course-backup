def find_prime(n):
    prime_list = [True] * n
    prime_list[0] = False
    prime_list[1] = False
    prime = list()
    for i in range(2, len(prime_list)):
        j = 2
        while i * j < len(prime_list):
            prime_list[i * j] = False
            j += 1
    for i in range(len(prime_list)):
        if prime_list[i] == True:
            prime.append(i)
            # print(i)
    return prime


p5d = list()
for i in find_prime(100000):
    if i > 10000:
        p5d.append(i)
# print(p5d)
for i in range(len(p5d) - 5):
    if p5d[i] == p5d[i + 1] - 2 and p5d[i + 1] == p5d[i + 2] - 4 and p5d[i + 2] == p5d[i + 3] - 6 and p5d[i + 3] == p5d[
                i + 4] - 8 and p5d[i + 4] == p5d[i + 5] - 10:
        rl=list()
        for j in range(6):
            rl.append(str(p5d[i+j]))
        print('  '.join(rl))

