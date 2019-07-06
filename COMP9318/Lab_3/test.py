## import modules here
from math import log, exp
################# Question 1 #################
import pandas as pd

raw_data = pd.read_csv('./asset/data.txt', sep='\t')
raw_data.head()


def tokenize(sms):
    return sms.split(' ')


def get_freq_of_tokens(sms):
    tokens = {}
    for token in tokenize(sms):
        if token not in tokens:
            tokens[token] = 1
        else:
            tokens[token] += 1
    return tokens


training_data = []
for index in range(len(raw_data)):
    training_data.append((get_freq_of_tokens(raw_data.iloc[index].text), raw_data.iloc[index].category))
def multinomial_nb(training_data, sms):# do not change the heading of the function
    #  **replace** this line with your code
    if len(training_data)==0:
        return
    ham_num = 0
    spam_num = 0
    for i in training_data:
        if i[-1] == 'ham':
            for j in i[0]:
                ham_num += i[0][j]
        else:
            for j in i[0]:
                spam_num += i[0][j]

    num_tol = len(set([v for msss in training_data for v in msss[0].keys()]))
    voc = set([v for msss in training_data for v in msss[0].keys()])
    #print(voc)

    Lham = 0
    Lspam = 0

    for i in sms:
        if i not in voc:
            continue
        word_total = 0
        word_ham = 0
        word_spam = 0
        # print(i)
        for j in training_data:
            if i in j[0]:
                word_total += j[0][i]
                if j[-1] == 'ham':
                    word_ham += 1
                else:
                    word_spam += 1

        pham = (word_ham + 1) / (ham_num + num_tol)
        print(word_ham + 1)
        print(ham_num + num_tol)
        pspam = (word_spam + 1) / (spam_num + num_tol)
        print(word_spam + 1)
        print(spam_num + num_tol)
        print(pham)
        print(pspam)
        Lham+=log(pham)
        Lspam+=log(pspam)

    numham = 0
    numspam = 0
    for i in training_data:
        #print(i[-1])
        if i[1] == 'ham':
            numham += 1
        else:
            numspam += 1

    pnumspam = numspam / len(training_data)
    print(numspam)
    print(len(training_data))

    s = exp(log(pnumspam)+Lspam-log(1-pnumspam)-Lham)
    s = pnumspam *exp(Lspam)/((1-pnumspam)*exp(Lham))
    print(pnumspam)
    print(1-pnumspam)
    print(exp(Lspam))
    print(exp(Lham))

    return s

sms = 'I am not spam'
print(multinomial_nb(training_data, tokenize(sms)))