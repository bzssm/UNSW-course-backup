#n个物体的重量(w[0]无用)
w = [5,8,13,27,14]
#n个物体的价值(p[0]无用)
p = [5,8,13,27,14]
#计算n的个数
n = len(w)
#背包的载重量
m = 33

dp = [[-1 for j in range(m + 1)] for i in range(n)]

for i in range(n):
    dp[i][0] = 0

for j in range(m + 1):
    if w[0] <= j:
        dp[0][j] = p[0]
    else:
        dp[0][j] = 0
print(dp)