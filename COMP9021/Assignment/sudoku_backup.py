from itertools import chain, combinations
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

        self.rowlist = deepcopy(self.originalStatus)
        self.collist = np.transpose(self.npMatrix).tolist()
        self.matlist = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                self.matlist.append(list(chain(*self.npMatrix[i:i + 3, j:j + 3].tolist())))

    '''
    +--------------------------+
    |                          |
    |Input check part          |
    |                          |
    +--------------------------+
    '''

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

    '''
    +--------------------------+
    |                          |
    |Output format part        |
    |                          |
    +--------------------------+
    '''

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
                '\\documentclass[10pt]{article}\n'
                '\\usepackage[left=0pt,right=0pt]{geometry}\n'
                '\\usepackage{tikz}\n'
                '\\usetikzlibrary{positioning}\n'
                '\\usepackage{cancel}\n'
                '\\pagestyle{empty}\n\n'
                '\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},\n'
                '                               label=above right:{\\tiny #2},\n'
                '                               label=below left:{\\tiny #3},\n'
                '                               label=below right:{\\tiny #4}]{#5};}}\n\n'
                '\\begin{document}\n\n'
                '\\tikzset{every node/.style={minimum size=.5cm}}\n\n'
                '\\begin{center}\n'
                '\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\\hline\\hline\n')
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
                    f.write('\\end{tabular}\n'
                            '\\end{center}\n\n'
                            '\\end{document}\n')

    '''
    +--------------------------+
    |                          |
    |Bare tex output part      |
    |                          |
    +--------------------------+
    '''

    def bare_tex_output(self):
        name = 'bare'
        self._generate_tex(name, fifth=list(chain(*self.originalStatus)))

    '''
    +--------------------------+
    |                          |
    |Forced tex output part    |
    |                          |
    +--------------------------+
    '''

    def _findbox(self, i, j):
        if i in range(3):
            if j in range(3):
                return 0
            elif j in range(3, 6):
                return 1
            elif j in range(6, 9):
                return 2
        elif i in range(3, 6):
            if j in range(3):
                return 3
            elif j in range(3, 6):
                return 4
            elif j in range(6, 9):
                return 5
        elif i in range(6, 9):
            if j in range(3):
                return 6
            elif j in range(3, 6):
                return 7
            elif j in range(6, 9):
                return 8

    def forced(self, status=None):
        if status == None:
            status = deepcopy(self.originalStatus)
        position = []
        marked_list = []
        matlist = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                matlist.append(list(chain(*np.array(status)[i:i + 3, j:j + 3].tolist())))

        for i in range(len(status)):
            for j in range(len(status)):
                used_set = set()
                for e in status[i]:
                    used_set.add(e)
                for e in np.transpose(np.array(status)).tolist()[j]:
                    used_set.add(e)
                for e in matlist[self._findbox(i, j)]:
                    used_set.add(e)
                if status[i][j] == '0':
                    marked_list.append(list(set(list('1234567890')) - used_set))
                else:
                    marked_list.append([])

        new_marked_list = []
        for i in range(9):
            new_marked_list.append(marked_list[9 * i:9 * i + 9])
        marked_list = new_marked_list
        box_marked_list = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                box_marked_list.append(list(chain(*np.array(marked_list)[i:i + 3, j:j + 3].tolist())))
        # print(box_marked_list)
        for box in box_marked_list:
            freq = Counter(chain(*box))
            for key in freq:
                if freq[key] == 1:
                    for cell in box:
                        if key in cell:
                            cell_num = box.index(cell)
                            box_num = box_marked_list.index(box)
                            position.append((box_num, cell_num))
                            status[(box_num // 3) * 3 + cell_num // 3][(box_num % 3) * 3 + cell_num % 3] = key
                            print(f'row:{(box_num//3)*3+cell_num//3},col:{(box_num%3)*3+cell_num%3},num = {key}')

        if 1 in list(chain(*[list(dict(Counter(list(chain(*box)))).values()) for box in box_marked_list])):
            self.forced(status=status)
        else:
            self.rowlist_forced = status
            self.collist_forced = np.transpose(np.array(status)).tolist()
            matlist = []
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    matlist.append(list(chain(*np.array(status)[i:i + 3, j:j + 3].tolist())))
            self.matlist_forced = matlist
        return self.rowlist_forced, position

    def forced_tex_output(self, status=None):
        status = self.forced(status)[0]
        name = 'forced'
        print(status)
        self._generate_tex(name, fifth=list(chain(*status)))

    '''
    +--------------------------+
    |                          |
    |Marked tex output part    |
    |                          |
    +--------------------------+
    '''

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
        i = 0
        first = [''] * 81
        second = [''] * 81
        third = [''] * 81
        forth = [''] * 81
        for row in marked_list:
            for cell in row:
                for e in cell:
                    if e in ['1', '2']:
                        first[i] += e
                    elif e in ['3', '4']:
                        second[i] += e
                    elif e in ['5', '6']:
                        third[i] += e
                    else:
                        forth[i] += e
                i += 1
        for i in range(len(first)):
            if len(first[i]) > 1:
                first[i] = ' '.join(sorted(list(first[i])))
        for i in range(len(second)):
            if len(second[i]) > 1:
                second[i] = ' '.join(sorted(list(second[i])))
        for i in range(len(third)):
            if len(third[i]) > 1:
                third[i] = ' '.join(sorted(list(third[i])))
        for i in range(len(forth)):
            if len(forth[i]) > 1:
                forth[i] = ' '.join(sorted(list(forth[i])))
        # print(first)
        self._generate_tex(name, first, second, third, forth, list(chain(*self.rowlist_forced)))
        self.marked_list = marked_list

    def _findpreemitiveset(self, originalmatrix, markedmatrix):
        def _findcellcount(preemptiveset, line):
            count = 0
            for cell in line:
                validcell = set(e for e in cell if len(e) == 1)
                if preemptiveset & validcell == validcell and len(validcell):
                    count += 1
            return count

        print(f'originalMatrix:\n{originalmatrix}')
        print(f'markedmatrix:\n{markedmatrix}')
        for line in markedmatrix:
            markedValue = chain(*line)
            possibleValue = set([e for e in markedValue if len(e) == 1])
            for i in range(2, len(possibleValue) + 1):
                possiblePreemptiveSet = set(combinations(possibleValue, i))
                for e in possiblePreemptiveSet:
                    if _findcellcount(set(e), line) == i:
                        for cell in line:
                            if set(ele for ele in cell if len(ele) == 1) & set(e) != set(
                                    ele for ele in cell if len(ele) == 1):
                                for value in e:
                                    if value in cell:
                                        cell[cell.index(value)] = '-' + cell[cell.index(value)]
        for linenum in range(len(markedmatrix)):
            for cellnum in range(len(markedmatrix[linenum])):
                if markedmatrix[linenum][cellnum] != []:
                    x = [e for e in markedmatrix[linenum][cellnum] if len(e) == 1]
                    if len(x) == 1:
                        originalmatrix[linenum][cellnum] = ''.join(x)
                        markedmatrix[linenum][cellnum][
                            markedmatrix[linenum][cellnum].index(''.join(x))] = '-' + ''.join(x)
                        for i in range(len(markedmatrix[linenum])):
                            if ''.join(x) in markedmatrix[linenum][i]:
                                markedmatrix[linenum][i][markedmatrix[linenum][i].index(''.join(x))] = '-' + ''.join(x)
                        for i in range(len(markedmatrix[cellnum])):
                            if ''.join(x) in markedmatrix[i][cellnum]:
                                markedmatrix[i][cellnum][markedmatrix[i][cellnum].index(''.join(x))] = '-' + ''.join(x)

                        matmark = []
                        for i in range(0, 9, 3):
                            for j in range(0, 9, 3):
                                matmark.append(list(chain(*np.array(markedmatrix)[i:i + 3, j:j + 3].tolist())))
                        markedmatrix = deepcopy(matmark)

                        for i in range(9):
                            if ''.join(x) in markedmatrix[self._findbox(linenum, cellnum)][i]:
                                markedmatrix[self._findbox(linenum, cellnum)][i][
                                    markedmatrix[self._findbox(linenum, cellnum)][i].index(''.join(x))] = '-' + ''.join(
                                    x)

                        matmark = []
                        for i in range(0, 9, 3):
                            for j in range(0, 9, 3):
                                matmark.append(list(chain(*np.array(markedmatrix)[i:i + 3, j:j + 3].tolist())))
                        markedmatrix = deepcopy(matmark)

        print(f'changedoriginalMatrix:\n{originalmatrix}')
        print(f'changedarkedmatrix:\n{markedmatrix}')
        return originalmatrix, markedmatrix

    def worked_tex_output(self):
        name = 'worked'
        self.marked_tex_output()
        rowmark = self.marked_list
        colmark = np.transpose(np.array(self.marked_list)).tolist()
        matmark = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                matmark.append(list(chain(*np.array(self.marked_list)[i:i + 3, j:j + 3].tolist())))

        # original status record
        matrix = deepcopy(self.rowlist_forced)
        count = 1
        while True:
            print('\ncount=', count, '\n')
            count += 1
            beforematrix = matrix
            beforemarked = rowmark
            # to row
            modifyedmatrix = deepcopy(matrix)
            modifyedmatrix, marklist = self._findpreemitiveset(modifyedmatrix, rowmark)

            # to colomn
            modifyedmatrix = np.transpose(np.array(modifyedmatrix)).tolist()
            marklist = np.transpose(np.array(marklist)).tolist()
            modifyedmatrix, marklist = self._findpreemitiveset(modifyedmatrix, marklist)
            modifyedmatrix = np.transpose(np.array(modifyedmatrix)).tolist()
            marklist = np.transpose(np.array(marklist)).tolist()

            # to box
            matmodifyedmatrix = []
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    matmodifyedmatrix.append(list(chain(*np.array(modifyedmatrix)[i:i + 3, j:j + 3].tolist())))
            modifyedmatrix = deepcopy(matmodifyedmatrix)

            # mark list to box
            matmarklist = []
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    matmarklist.append(list(chain(*np.array(marklist)[i:i + 3, j:j + 3].tolist())))
            marklist = deepcopy(matmarklist)
            modifyedmatrix, marklist = self._findpreemitiveset(modifyedmatrix, marklist)

            matmodifyedmatrix = []
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    matmodifyedmatrix.append(list(chain(*np.array(modifyedmatrix)[i:i + 3, j:j + 3].tolist())))
            modifyedmatrix = deepcopy(matmodifyedmatrix)
            matmarklist = []
            for i in range(0, 9, 3):
                for j in range(0, 9, 3):
                    matmarklist.append(list(chain(*np.array(marklist)[i:i + 3, j:j + 3].tolist())))
            marklist = deepcopy(matmarklist)

            matrix = modifyedmatrix
            rowmark = marklist

            if matrix == beforematrix and rowmark == beforemarked:
                modifyedmatrix, changedpositions = self.forced(matrix)
                if changedpositions != []:
                    for position in changedpositions:
                        changedrow = (position[0] // 3) * 3 + position[1] // 3
                        changedcol = (position[0] % 3) * 3 + position[1] % 3
                        changedval = modifyedmatrix[changedrow][changedcol]
                        for i in range(9):
                            if changedval in marklist[changedrow][i]:
                                marklist[changedrow][i][
                                    marklist[changedrow][i].index(changedval)] = '-' + changedval
                        for i in range(9):
                            if changedval in marklist[i][changedcol]:
                                marklist[i][changedcol][
                                    marklist[i][changedcol].index(changedval)] = '-' + changedval
                        newmarklist = []
                        for i in range(0, 9, 3):
                            for j in range(0, 9, 3):
                                newmarklist.append(
                                    list(chain(*np.array(marklist)[i:i + 3, j:j + 3].tolist())))
                        marklist = deepcopy(newmarklist)

                        for i in range(9):
                            if changedval in marklist[self._findbox(changedcol, changedcol)][i]:
                                marklist[self._findbox(changedcol, changedcol)][i][
                                    marklist[self._findbox(changedcol, changedcol)][i].index(
                                        changedval)] = '-' + changedval

                        newmarklist = []
                        for i in range(0, 9, 3):
                            for j in range(0, 9, 3):
                                newmarklist.append(
                                    list(chain(*np.array(marklist)[i:i + 3, j:j + 3].tolist())))
                        marklist = deepcopy(newmarklist)

                        matrix = modifyedmatrix
                        rowmark = marklist
                else:
                    break



        print(f'Matrix:\n{matrix}')
        print(f'markedmatrix:\n{rowmark}')

        i = 0
        first = [''] * 81
        second = [''] * 81
        third = [''] * 81
        forth = [''] * 81
        for row in rowmark:
            for cell in row:

                for e in cell:
                    if str(abs(int(e))) in ['1', '2']:
                        first[i] = first[i] + e + ','
                    elif str(abs(int(e))) in ['3', '4']:
                        second[i] = second[i] + e + ','
                    elif str(abs(int(e))) in ['5', '6']:
                        third[i] = third[i] + e + ','
                    else:
                        forth[i] = forth[i] + e + ','

                i += 1

        # print(first)
        def formatlist(l):
            for i in range(len(l)):
                l[i] = l[i].rstrip(',')
                l[i] = l[i].split(',')
                if l[i] == ['']:
                    l[i] = ''
                    continue
                for k in range(len(l[i])):
                    l[i][k] = int(l[i][k])
                l[i] = sorted(l[i], key=abs)
                for k in range(len(l[i])):
                    l[i][k] = str(l[i][k])
                for k in range(len(l[i])):
                    if len(l[i][k]) > 1:
                        l[i][k] = '\\cancel{' + str(abs(int(l[i][k]))) + '}'
                l[i] = ' '.join(l[i])
            return l

        first = formatlist(first)
        second = formatlist(second)
        third = formatlist(third)
        forth = formatlist(forth)
        # print(first)
        self._generate_tex(name, first, second, third, forth, list(chain(*matrix)))
