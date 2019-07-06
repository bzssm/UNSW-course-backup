import sys

word_to_value = {'a': 2, 'b': 5, 'c': 4, 'd': 4, 'e': 1, 'f': 6, \
                 'g': 5, 'h': 5, 'i': 1, 'j': 7, 'k': 6, 'l': 3, \
                 'm': 5, 'n': 2, 'o': 3, 'p': 5, 'q': 7, 'r': 2, \
                 's': 1, 't': 2, 'u': 4, 'v': 6, 'w': 6, 'x': 7, \
                 'y': 5, 'z': 7}


def load():
    with open('wordsEn.txt', 'r') as f:
        words = [w.replace('\n', '') for w in f]
        # print('word size =', len(words))
        return words


def value_cal(word, input_set):
    value = 0
    for character in word:
        if input_set.count(character) >= word.count(character) and character in input_set:
            value += word_to_value[character]
        else:
            return False, 0
    return True, value


def loop(words, input_set):
    result_dic = dict()
    for word in words:
        flag, value = value_cal(word, input_set)
        if flag == True:
            result_dic[word] = value
    if result_dic == {}:
        return None, None
    result_list = sorted(result_dic.items(), key=lambda d: d[1], reverse=True)
    max_value = result_list[0][1]
    max_value_word = [l[0] for l in result_list if l[1] == max_value]
    return max_value_word, max_value


def input_part():
    input_string = input('Enter between 3 and 10 lowercase letters: ')
    # print (input_string.replace(' ',''))
    if len(input_string.replace(' ', '')) <= 10 and len(input_string.replace(' ', '')) >= 3:
        for c in input_string.replace(' ', ''):
            if c in word_to_value.keys():
                continue
            else:
                print('Incorrect input, giving up...')
                sys.exit()
                break
        return [character for character in input_string.replace(' ', '')]
    else:
        print('Incorrect input, giving up...')
        sys.exit()


words = load()
input_letter_list = input_part()
max_value_word, max_value = loop(words, input_letter_list)
if max_value == None:
    print('No word is built from some of those letters.')
else:
    print(f'The highest score is {max_value}.')
    if len(max_value_word) == 1:
        print(f'The highest scoring word is {max_value_word[0]}')
    else:
        print('The highest scoring words are, in alphabetical order:')
        for word in max_value_word:
            print('\t', word)

# print(input_letter_list)
