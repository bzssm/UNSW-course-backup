import random
from collections import defaultdict


class Target:
    def __init__(self, dictionary='dictionary.txt', target=None, minimal_length=4):
        self.dictionary = set()
        with open(dictionary) as f:
            lines = f.readlines()
            for l in lines:
                if len(set(l.replace('\n', ''))) == len(l.replace('\n', '')):
                    self.dictionary.add(l.replace('\n', ''))
        self.target = target
        self.minimal_length = minimal_length
        self.targetDictionary = set()
        for e in self.dictionary:
            if len(e) == 9:
                self.targetDictionary.add(e)
        if self.target:
            target_letters = []
            for e in self.targetDictionary:
                target_letters.append(set(e))
            if set(self.target) not in target_letters:
                self.target = None

        if not self.target:
            self.target = random.choice(list(self.targetDictionary))
        self.targetList = list(set(self.target))
        self.FindSolutions()
        # print(self.solutions)

    def __repr__(self):
        return f'Target(dictionary = {self.dictionary}, minimal_length = {self.minimal_length}'

    def __str__(self):
        return '       ___________\n\n' + \
               f'      | {self.targetList[0]} | {self.targetList[1]} | {self.targetList[2]} |\n' + \
               '       ___________\n\n' + \
               f'      | {self.targetList[3]} | {self.targetList[4]} | {self.targetList[5]} |\n' + \
               '       ___________\n\n' + \
               f'      | {self.targetList[6]} | {self.targetList[7]} | {self.targetList[8]} |\n' + \
               '       ___________\n'

    def FindSolutions(self):
        self.solutions = defaultdict(list)
        for e in self.dictionary:
            if self.targetList[4] in set(e) and set(e) & set(self.targetList) == set(e) and len(
                    e) >= self.minimal_length and len(e) <= 9:
                self.solutions[len(e)].append(e)

    def number_of_solutions(self):
        print(f'In decreasing order of length between 9 and {self.minimal_length}:')
        for e in sorted(self.solutions.items(), key=lambda x: x[0], reverse=True):
            if len(self.solutions[e[0]]) == 1:
                print(f'    {len(self.solutions[e[0]])} solution of length {e[0]}')
            else:
                print(f'    {len(self.solutions[e[0]])} solutions of length {e[0]}')

    def give_solutions(self, length=0):
        for e in sorted(self.solutions.items(), key=lambda x: x[0], reverse=True):
            if e[0] >= length:
                if len(self.solutions[e[0]]) == 1:
                    print(f'Solution of length {e[0]}:')
                else:
                    print(f'Solutions of length {e[0]}:')
                print('\n'.join(sorted('    ' + s for s in self.solutions[e[0]])))
                if e[0] != min(n - length for n in self.solutions.keys() if n >= length) + length:
                    print()

    def change_target(self, to_be_replaced, to_replace):
        if to_be_replaced == to_replace or set(to_be_replaced) & set(self.target) != set(to_be_replaced) or len(
                to_be_replaced) != len(to_replace):
            print('The target was not changed.')
            return


        target_backup1 = self.target
        target_letters = []
        for e in self.targetDictionary:
            target_letters.append(set(e))
        for e in to_be_replaced:
            target_backup1.replace(e, to_replace[to_be_replaced.index(e)])
        if set(target_backup1) not in target_letters:
            print('The target was not changed')
            return


        target_backup = self.target
        self.target = self.target.translate(str.maketrans(to_be_replaced, to_replace))
        if set(target_backup)==set(self.target) and target_backup[4]==self.target[4]:
            print('The solutions are not changed')
        self.targetList = list(set(self.target))
        self.FindSolutions()


