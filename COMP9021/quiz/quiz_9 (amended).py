# Generates a binary tree T whose shape is random and whose nodes store
# random even positive integers, both random processes being directed by user input.
# With M being the maximum sum of the nodes along one of T's branches, minimally expands T
# to a tree T* such that:
# - every inner node in T* has two children, and
# - the sum of the nodes along all of T*'s branches is equal to M.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, randrange
from collections import deque


from quiz.binary_tree_adt import *


def create_tree(tree, for_growth, bound):
    if randrange(max(for_growth, 1)):
        tree.value = 2 * randrange(bound + 1)
        tree.left_node = BinaryTree()
        tree.right_node = BinaryTree()
        create_tree(tree.left_node, for_growth - 1, bound)
        create_tree(tree.right_node, for_growth - 1, bound)


def expand_tree(tree):
    if tree.height()<1:
        return tree
    maxvalue,son_father,nodelist = dfs(tree)
    for e in nodelist:
        if e.left_node.value!=None and e.right_node.value!=None:
            continue
        currentsum = sum(backtrack(tree,son_father,e))
        if currentsum == maxvalue:
            continue
        if e.left_node.value ==None:
            e.left_node = BinaryTree(maxvalue - currentsum)
        if e.right_node.value ==None:
            e.right_node = BinaryTree(maxvalue - currentsum)


def dfs(tree):
    queue = []
    queue.append(tree)
    son_father = {}
    lastnode = []
    nodelist=[]
    while len(queue):
        node = queue.pop()
        nodelist.append(node)
        # print(node.value)
        subnodes = [e for e in [node.left_node, node.right_node] if e.value != None]
        if subnodes == []:
            lastnode.append(node)
            continue
        for e in subnodes:
            queue.append(e)
            son_father[e] = node
        # print([(e[0].value, e[1].value) for e in list(son_father.items())])
        subnodes = []
    # print(son_father)
    # print([e.value for e in lastnode])
    sumpath = []
    for e in lastnode:
        sumpath.append((backtrack(tree, son_father, e), sum(backtrack(tree, son_father, e))))
    # print(sumpath)
    maxvalue = max(sumpath, key=lambda x: x[1])
    return maxvalue[1],son_father,nodelist


def backtrack(tree, son_father, lastnode):
    path = [lastnode]
    while path[-1] != tree:
        path.append(son_father[path[-1]])
    return [e.value for e in path]


try:
    for_seed, for_growth, bound = [int(x) for x in input('Enter three positive integers: ').split()
                                   ]
    if for_seed < 0 or for_growth < 0 or bound < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
tree = BinaryTree()
create_tree(tree, for_growth, bound)
print('Here is the tree that has been generated:')
tree.print_binary_tree()
expand_tree(tree)
print('Here is the expanded tree:')
tree.print_binary_tree()
