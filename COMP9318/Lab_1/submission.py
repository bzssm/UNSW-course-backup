## import modules here


################# Question 0 #################

def add(a, b):  # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x):  # do not change the heading of the function
    a = x
    b = (x + 1) // 2
    while b < a:
        a = b
        b = (a + x // a) // 2
    return a


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them


def find_root(f, fprime, x_0=1.0, EPSILON=1E-7, MAX_ITER=1000):  # do not change the heading of the function
    x_value = [x_0, x_0 - (f(x_0) / fprime(x_0))]

    while abs(x_value[-1] - x_value[-2]) > EPSILON and len(x_value) < MAX_ITER + 2:
        x_value.append(x_value[-1] - f(x_value[-1]) / fprime(x_value[-1]))
    return x_value[-1]


################# Question 3 #################


class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)


def make_tree(tokens):  # do not change the heading of the function
    stack = []
    for e in tokens:
        if e != ']':
            stack.append(e)
        else:
            children = []
            while stack[-1] != '[':
                children.append(stack.pop())
            children.reverse()
            stack.pop()
            parent = stack.pop()
            if not isinstance(parent, Tree):
                parent = Tree(parent)
            for e in children:
                if not isinstance(e, Tree):
                    parent.add_child(Tree(e))
                else:
                    parent.add_child(e)
            stack.append(parent)
    return stack[0]


def max_depth(root):  # do not change the heading of the function
    temp = []
    res = 1
    if root.children:
        scan = root.children
    else:
        return res
    while any([e.children for e in scan]):
        res += 1
        for e in scan:
            temp += e.children
        scan = temp
        temp = []
    return res + 1
