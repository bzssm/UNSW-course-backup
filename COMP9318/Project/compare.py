import itertools
from collections import defaultdict, OrderedDict

import Project.helper
from Project import helper
from Project.submission import merge

ins = Project.helper.strategy()

d=ins.check_data('test_data.txt','modified_data.txt')
print(d)

res = defaultdict(tuple)
f = merge(['class-0.txt', 'class-1.txt'])
strategy_instance = helper.strategy()
parameters = {}
# initial parameters
parameters['gamma'] = 'auto'
parameters['C'] = 0.95
parameters['kernel'] = 'linear'
parameters['degree'] = 3
parameters['coef0'] = 0.0
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english', binary=True)  # ,min_df=2,max_df=0.8,max_features=240)
vectorizer.fit(f)
X_train = vectorizer.transform(f)
X_test = vectorizer.transform(open('modified_data.txt', 'r'))
Y_train = ['class-0'] * 360 + ['class-1'] * 180
Y_test = ['class-0'] * 200
clf = strategy_instance.train_svm(parameters, X_train, Y_train)
words = vectorizer.vocabulary_.keys()
words_index = dict([e[::-1] for e in vectorizer.vocabulary_.items()])
coef = list(clf.coef_.toarray().tolist()[0])
print(coef)
words_coef = {}
for i in words_index:
    words_coef[words_index[i]] = coef[i]
# print(sorted(words_coef.items(),key=lambda x:x[1],reverse=True))
words_postion = OrderedDict(
    zip([e[0] for e in sorted(words_coef.items(), key=lambda x: x[1])], itertools.count(0)))
print(words_postion)
for e in d:
    print(words_postion[e])