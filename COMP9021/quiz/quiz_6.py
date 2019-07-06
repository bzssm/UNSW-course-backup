# Creates a class to represent a permutation of 1, 2, ..., n for some n >= 0.
#
# An object is created by passing as argument to the class name:
# - either no argument, in which case the empty permutation is created, or
# - "length = n" for some n >= 0, in which case the identity over 1, ..., n is created, or
# - the numbers 1, 2, ..., n for some n >= 0, in some order, possibly together with "lengh = n".
#
# __len__(), __repr__() and __str__() are implemented, the latter providing the standard form
# decomposition of the permutation into cycles (see wikepedia page on permutations for details).
#
# Objects have:
# - nb_of_cycles as an attribute
# - inverse() as a method
#
# The * operator is implemented for permutation composition, for both infix and in-place uses.
#
# Written by *** and Eric Martin for COMP9021


class PermutationError(Exception):
    def __init__(self, message):
        self.message = message


class Permutation:
    def __init__(self, *args, length=None):
        if length == None:
            if not all(isinstance(i, int) for i in args):
                raise PermutationError('Cannot generate permutation from these arguments')
        else:
            if len(args) != 0:
                if length != len(args):
                    raise PermutationError('Cannot generate permutation from these arguments')
            else:
                if length < 1:
                    raise PermutationError('Cannot generate permutation from these arguments')
                else:
                    args = tuple(i + 1 for i in range(length))
        if any(i < 1 for i in args):
            raise PermutationError('Cannot generate permutation from these arguments')
        if set(args) != set(range(1, len(args) + 1)):
            raise PermutationError('Cannot generate permutation from these arguments')
        self._number = args
        self._cycle_list = self._get_cycles()
        self.nb_of_cycles = len([e for e in self._cycle_list if e != ()])

    def _get_cycles(self):

        def modify_seq(l):
            for i in range(len(l)):
                l[i] = l[i][l[i].index(max(l[i])):] + l[i][:l[i].index(max(l[i]))]
            return sorted([tuple(e) for e in l], key=lambda x: x[0])

        cycle_list = list(self._number)
        result = []
        record = [False] * len(self._number)
        current_position = 0
        result.append([])
        for _ in range(len(cycle_list)):
            result[len(result) - 1].append(cycle_list[current_position])
            record[current_position] = True
            current_position = cycle_list[current_position] - 1
            if record[current_position] == True:
                result.append([])
                if any(e == False for e in record):
                    current_position = min(i for i in range(len(record)) if record[i] == False)
        result.pop()
        if len(result) != 0:
            return modify_seq(result)
        else:
            return [()]

    def __len__(self):
        return len(self._number)

    def __repr__(self):
        return f'Permutation{self._number}'

    def __str__(self):
        l = self._cycle_list
        result = ''
        for i in range(len(l)):
            l[i] = list(l[i])
            l[i] = "(" + ' '.join([str(e) for e in l[i]]) + ")"
        return ''.join(l)

    def __mul__(self, permutation):
        if len(self) != len(permutation):
            raise PermutationError('Cannot compose permutations of different lengths')
        else:
            result_list = []
            for i in range(len(self)):
                result_list.append(permutation._number[self._number[i] - 1])
            return Permutation(*tuple(result_list))

    def __imul__(self, permutation):
        return self * permutation
        # Replace pass above with your code

    def inverse(self):
        result_list = []
        for i in range(1, len(self._number) + 1):
            result_list.append(self._number.index(i) + 1)
        return Permutation(*tuple(result_list))
