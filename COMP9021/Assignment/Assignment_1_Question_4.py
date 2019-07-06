import random
from collections import Counter, defaultdict, OrderedDict

order_seq = ['Five of a kind', 'Four of a kind', 'Full house', 'Straight', 'Three of a kind', 'Two pair', 'One pair',
             'Bust']


def number_to_name(number):
    dic = {0: 'Ace', 1: 'King', 2: 'Queen', 3: 'Jack', 4: '10', 5: '9'}
    return dic[number]


def name_to_number(name):
    dic = {'Ace': 0, 'King': 1, 'Queen': 2, 'Jack': 3, '10': 4, '9': 5}
    return dic[name]


def first_roll():
    roll_list = [random.randint(0, 5) for _ in range(5)]
    roll_list.sort()
    roll_name_list = [number_to_name(e) for e in roll_list]
    # print(' '.join(roll_name_list))
    return roll_list


def status_judge(status):
    statistic = Counter(status)
    statistic_counter = sorted(list(statistic.values()), reverse=True)
    printstring = None
    if statistic_counter == [5]:
        printstring = 'It is a Five of a kind'
    elif statistic_counter == [4, 1]:
        printstring = 'It is a Four of a kind'
    elif statistic_counter == [3, 2]:
        printstring = 'It is a Full house'
    elif statistic_counter == [3, 1, 1]:
        printstring = 'It is a Three of a kind'
    elif statistic_counter == [2, 2, 1]:
        printstring = 'It is a Two pair'
    elif statistic_counter == [2, 1, 1, 1]:
        printstring = 'It is a One pair'
    elif statistic_counter == [1, 1, 1, 1, 1]:
        if status == [0, 1, 2, 3, 4] or status == [1, 2, 3, 4, 5]:
            printstring = 'It is a Straight'
        else:
            printstring = 'It is a Bust'
    # print(statistic_counter)
    # print(printstring)
    return printstring


def isValid(status, keep_name_list):
    for e in keep_name_list:
        try:
            if keep_name_list.count(e) <= status.count(name_to_number(e)):
                continue
            else:
                return False
        except KeyError:
            return False
    return True


def reroll(status, time):
    flag = True
    while flag:
        keep_name = input(f'Which dice do you want to keep for the {time} roll? ')
        keep_name_list = keep_name.split(' ')
        if keep_name.strip() == 'all' or keep_name.strip() == 'All' or sorted(keep_name_list) == sorted(
                [number_to_name(e) for e in status]):
            print('Ok, done.')
            return status, 'done'
        else:
            if keep_name == '':
                return_list = sorted([random.randint(0, 5) for _ in range(5)])
                print(f'The roll is: ' + ' '.join([number_to_name(e) for e in return_list]))
                print(status_judge(return_list))
                return return_list, 'cont'
            elif isValid(status, keep_name_list):
                return_list = [name_to_number(e) for e in keep_name_list]
                return_list.extend([random.randint(0, 5) for _ in range(5 - len(return_list))])
                return_list.sort()
                print(f'The roll is: ' + ' '.join([number_to_name(e) for e in return_list]))
                print(status_judge(return_list))
                return return_list, 'cont'
            else:
                print('That is not possible, try again!')


def play():
    status = first_roll()
    print(f'The roll is: ' + ' '.join([number_to_name(e) for e in status]))
    print(status_judge(status))
    status, isContinue = reroll(status, 'second')
    if isContinue == 'done':
        return status
    elif isContinue == 'cont':
        status, isContinue = reroll(status, 'third')
        return status
    return status


def simulate(time):
    result_dic = dict()
    for e in order_seq:
        result_dic.setdefault('It is a '+e,0)

    for _ in range(time):
        result_dic[status_judge(first_roll())] += 1
    result_dic = OrderedDict(sorted(result_dic.items(), key=lambda x: order_seq.index(x[0].replace('It is a ', ''))))

    for e in order_seq:
        if e != 'Bust':
            print('%-15s: %.2f' % (e.replace('It is a ', ''), 100*result_dic['It is a '+e] / time)+'%')
            print('%-15s: %f' % (e.replace('It is a ', ''), 100 * result_dic['It is a ' + e] / time) + '%')
            # print(f"{(e.replace('It is a ','')):-16s}\t: {(result_dic[e]/time):.2f}")


if __name__ == '__main__':
    random.seed(500)
    simulate(200000)
