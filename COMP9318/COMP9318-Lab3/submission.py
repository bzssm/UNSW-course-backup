## import modules here
from collections import Counter
################# Question 1 #################
import pandas as pd

def preprocess(training_data):
    res = {}
    for e in training_data:
        if e[1] not in res:
            res[e[1]] = e[0]
        else:
            res[e[1]] = Counter(res[e[1]]) + Counter(e[0])
    return res


def multinomial_nb(training_data, sms):  # do not change the heading of the function
    res = 1
    data_set = preprocess(training_data)
    print(data_set)

    hamnum = 0
    spamnum = 0
    for e in training_data:
        if e[1] == 'ham':
            hamnum += 1
        else:
            spamnum += 1

    for e in sms:
        if e not in set().union(list(data_set['ham'].keys()), list(data_set['spam'].keys())):
            continue
        hamp = (data_set['ham'][e] + 1) / (sum(data_set['ham'].values()) + len(
            set().union(list(data_set['ham'].keys()), list(data_set['spam'].keys()))))
        spamp = (data_set['spam'][e] + 1) / (
                    sum(data_set['spam'].values()) + len(set().union(data_set['ham'].keys(), data_set['spam'].keys())))
        res = res * spamp / hamp
    return res * spamnum / hamnum
