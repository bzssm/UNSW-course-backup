from collections import deque


def printgrid(grid):
    strgrid = str(grid)
    i = 0
    for c in strgrid:
        if c != '9':
            print(c, end=' ')
        else:
            print(' ', end=' ')
        i += 1
        if i % 3 == 0:
            print()
    print()


def grid2int(grid):
    res = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            res.append(str(grid[i][j]))
    return list2int(res)


def pregrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0 or grid[i][j] == None:
                grid[i][j] = 9
    # print(grid)
    return (grid)


def list2int(seq):
    result = 0
    # print(seq)
    for i in range(len(seq)):
        if seq[i]=='None':
            seq[i]='9'
        result += int(seq[i]) * (10 ** (len(seq) - i - 1))
    return result


def subnodes(number):
    chain = []
    for i in str(number):
        chain.append(i)
    # print(chain)
    backup = list(chain)
    result = []
    changeDict = {0: {1, 3}, 1: {0, 2, 4}, 2: {1, 5},
                  3: {0, 4, 6}, 4: {1, 3, 5, 7}, 5: {2, 4, 8},
                  6: {3, 7}, 7: {4, 6, 8}, 8: {5, 7}
                  }
    for i in changeDict[chain.index('9')]:
        chain[chain.index('9')], chain[i] = chain[i], chain[chain.index('9')]
        result.append(chain)
        chain = list(backup)
    return [list2int(e) for e in result]


def backtrace(startNode, soughtValue, path1):
    path = [soughtValue]
    while (path[-1] != startNode):
        path.append(path1[path[-1]])
    return path


def bfs(startNode, soughtValue=123456789):
    usedNode = set()
    path1 = {}
    queue = deque([startNode])
    # print(queue)
    while len(queue) > 0:
        node = queue.pop()
        if node in usedNode:
            continue
        usedNode.add(node)
        # print(node)
        if node == soughtValue:
            return backtrace(startNode, soughtValue, path1)
        for n in subnodes(node):
            if n not in usedNode:
                queue.appendleft(n)
                path1[n] = node
                # print(f'n: {n},  father: {node}')
    return False


def validate_9_puzzle(grid):
    # print([i for i in range(len(grid)) if len(grid[i]) != 3])
    # print(grid2int(pregrid(grid)))
    # print(bfs(grid2int(pregrid(grid))))
    # print(set([e for e in str(grid2int(grid))]))
    if len(grid) == 3 and [i for i in range(len(grid)) if len(grid[i]) != 3] == []:
        if set([int(e) for e in str(grid2int(grid))]) == {1, 2, 3, 4, 5, 6, 7, 8, 9} and bfs(
                grid2int(pregrid(grid))) != False:
            print('This is a valid 9 puzzle, and it is solvable')
        else:
            print('This is an invalid or unsolvable 9 puzzle')
    else:
        print('This is an invalid or unsolvable 9 puzzle')


def solve_9_puzzle(grid):
    if grid == [[1, 2, 3], [4, 5, 6], [7, 8, 0]] or grid == [[1, 2, 3], [4, 5, 6], [7, 8, None]]:
        printgrid(grid)
    else:
        res = bfs(grid2int(pregrid(grid)))
        res.reverse()
        for e in res:
            printgrid(e)


validate_9_puzzle([[1, 2, 3], [4, 5, 6], [None, 7, 8]])


# start = [[4, None, 8], [1, 3, 7], [5, 2, 6]]
# final = 123456789
# # print(pregrid(start))
# print(grid2int(pregrid(start)))
# res=bfs(grid2int(pregrid(start)),final)
# res.reverse()
# for e in res:
#     printgrid(e)
