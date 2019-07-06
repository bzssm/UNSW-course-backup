from itertools import chain
import numpy as np
from copy import deepcopy
from collections import Counter


class SudokuError(Exception):
    def __init__(self, message):
        self.message = message


class Sudoku:
    def __init__(self, path):
        self.path = path
        self._checkinput()
        rowlist = deepcopy(self.originalStatus)
        collist = np.transpose(self.npMatrix).tolist()
        matlist = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                matlist.append(list(chain(*self.npMatrix[i:i + 3, j:j + 3].tolist())))
        self.rowlist = rowlist
        self.collist = collist
        self.matlist = matlist
        self.rowlist_forced = rowlist
        self.collist_forced = collist
        self.matlist_forced = matlist

    def _checkinput(self):
        self.originalStatus = []
        with open(self.path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace(' ', '').replace('\n', '')
                if line:
                    self.originalStatus.append(list(line))
        self.npMatrix = np.array(self.originalStatus)
        if self.npMatrix.shape == (9, 9) and all(e in '1234567890' for e in list(chain(*self.originalStatus))):
            print('Correct')
        else:
            raise SudokuError('Incorrect input')
        '''        
        if len(self.originalStatus) == 9 and all(len(e) == 9 for e in self.originalStatus) and \
                all(e in '0123456789' for e in list(chain(*self.originalStatus))):
            print('Correct')
        else:
            raise SudokuError('Incorrect input')
        '''

    def preassess(self):

        rowlistdic = list(map(dict, list(map(Counter, self.rowlist))))
        collistdic = list(map(dict, list(map(Counter, self.collist))))
        matlistdic = list(map(dict, list(map(Counter, self.matlist))))
        for e in rowlistdic + collistdic + matlistdic:
            e.pop('0')
            if set(e.values()) != {1} and list(e.values()) != []:
                print('There is clearly no solution.')
                break
        else:
            print('There might be a solution.')


    def _datatotex(self, first, second, third, forth, fifth):
        if first == '0':
            first = ''
        if second == '0':
            second = ''
        if third == '0':
            third = ''
        if forth == '0':
            forth = ''
        if fifth == '0':
            fifth = ''
        return '\\' + 'N{' + first + '}' + '{' + second + '}' + '{' + third + '}' + '{' + forth + '}' + '{' + fifth + '}'

    def _generate_tex(self, name, first=[''] * 81, second=[''] * 81, third=[''] * 81, forth=[''] * 81, fifth=[''] * 81):
        # print(first)
        # print(second)
        with open(self.path.rstrip('.txt') + '_' + name + '.tex', 'w') as f:
            f.write(
                '\\documentclass[10pt]{article}\n\\usepackage[left=0pt,right=0pt]{geometry}\n\\usepackage{tikz}\n\\usetikzlibrary{positioning}\n\\usepackage{cancel}\n\\pagestyle{empty}\n\n\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},\n                               label=above right:{\\tiny #2},\n                               label=below left:{\\tiny #3},\n                               label=below right:{\\tiny #4}]{#5};}}\n\n\\begin{document}\n\n\\tikzset{every node/.style={minimum size=.5cm}}\n\n\\begin{center}\n\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\\hline\\hline\n')
            for i in range(9):
                f.write(f'% Line {i+1}\n')
                for j in range(9 * i, 9 + 9 * i):
                    # print(j)
                    f.write(self._datatotex(first[j], second[j], third[j], forth[j], fifth[j]))
                    if j % 3 == 0 or j % 3 == 1:
                        f.write(' & ')
                    elif j % 9 == 2 or j % 9 == 5:
                        f.write(' &\n')
                    elif j % 9 == 8 and i % 3 != 2:
                        f.write(' \\\\ \\hline\n')
                    elif j % 9 == 8 and i % 3 == 2:
                        f.write(' \\\\ \\hline\\hline\n')
                if i != 8:
                    f.write('\n')
                else:
                    f.write('\\end{tabular}\n\\end{center}\n\n\\end{document}\n')

    def bare_tex_output(self):
        name = 'bare'
        self._generate_tex(name, fifth=list(chain(*self.originalStatus)))

    def _findbox(self,i,j):
        if i in range(3):
            if j in range(3):
                return 0
            elif j in range(3,6):
                return 1
            elif j in range(6,9):
                return 2
        elif i in range(3,6):
            if j in range(3):
                return 3
            elif j in range(3,6):
                return 4
            elif j in range(6,9):
                return 5
        elif i in range(6,9):
            if j in range(3):
                return 6
            elif j in range(3,6):
                return 7
            elif j in range(6,9):
                return 8

    def _updateforcedstatus(self,status):
        self.rowlist_forced = deepcopy(status)
        self.collist_forced = np.transpose(np.array(status)).tolist()
        self.matlist_forced = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                self.matlist_forced.append(list(chain(*np.array(status)[i:i + 3, j:j + 3].tolist())))

    def forced_tex_output(self,status = None):
        if status==None:
            status = deepcopy(self.originalStatus)
        name = 'forced'
        marked_list = []
        for i in range(9):
            for j in range(9):
                used_set=set()
                for e in self.rowlist_forced[i]:
                    used_set.add(e)
                for e in self.collist_forced[j]:
                    used_set.add(e)
                for e in self.matlist_forced[self._findbox(i,j)]:
                    used_set.add(e)
                if status[i][j]=='0':
                    marked_list.append(list(set([str(e) for e in range(10)])-used_set))
                else:
                    marked_list.append([])

        new_marked_list = []
        for i in range(9):
            new_marked_list.append(marked_list[9*i:9+9*i])
        marked_list = new_marked_list
        box_marked_list=[]
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box_marked_list.append(list(chain(*np.array(marked_list)[i:i + 3, j:j + 3].tolist())))
        fifth = deepcopy(status)
        for box in box_marked_list:
            freq=dict(Counter(list(chain(*box))))
            for key in freq:
                if freq[key]==1:
                    for cell in box:
                        if key in cell:
                            cell_num = box.index(cell)
                            box_num = box_marked_list.index(box)
                            fifth[(box_num//3)*3+cell_num//3][(box_num%3)*3+cell_num%3] = key
                            print(f'row:{(box_num//3)*3+cell_num//3},col:{(box_num%3)*3+cell_num%3},num = {key}')

        self._updateforcedstatus(fifth)
        if 1 in list(chain(*[list(dict(Counter(list(chain(*box)))).values()) for box in box_marked_list])):
            self.forced_tex_output(status = fifth)
        else:
            self._generate_tex(name, fifth=list(chain(*fifth)))

    def marked_tex_output(self):
        name = 'marked'
        self.forced_tex_output()
        marked_list = []
        for i in range(9):
            for j in range(9):
                used_set = set()
                for e in self.rowlist_forced[i]:
                    used_set.add(e)
                for e in self.collist_forced[j]:
                    used_set.add(e)
                for e in self.matlist_forced[self._findbox(i, j)]:
                    used_set.add(e)
                if self.rowlist_forced[i][j] == '0':
                    marked_list.append(list(set([str(e) for e in range(10)]) - used_set))
                else:
                    marked_list.append([])

        new_marked_list = []
        for i in range(9):
            new_marked_list.append(marked_list[9 * i:9 + 9 * i])
        marked_list = new_marked_list
        i=0
        first=['']*81
        second=['']*81
        third=['']*81
        forth=['']*81
        for row in marked_list:
            for cell in row:
                for e in cell:
                    if e in ['1','2']:
                        first[i]+=e
                    elif e in ['3','4']:
                        second[i]+=e
                    elif e in ['5','6']:
                        third[i]+=e
                    else:
                        forth[i]+=e
                i+=1
        for i in range(len(first)):
            if len(first[i])>1:
                first[i] = ' '.join(sorted(list(first[i])))
        for i in range(len(second)):
            if len(second[i])>1:
                second[i] = ' '.join(sorted(list(second[i])))
        for i in range(len(third)):
            if len(third[i])>1:
                third[i] = ' '.join(sorted(list(third[i])))
        for i in range(len(forth)):
            if len(forth[i])>1:
                forth[i] = ' '.join(sorted(list(forth[i])))
        print(first)
        self._generate_tex(name,first,second,third,forth,list(chain(*self.rowlist_forced)))

