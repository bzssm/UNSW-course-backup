from Lab_7.target import *

test = Target(target = 'IMRVOZATK', minimal_length = 5)
print(test)
test.number_of_solutions()
test.give_solutions(5)
test.change_target('MARKOVITZ', 'ABCDEFGHI')
print(test)
test.give_solutions(5)


