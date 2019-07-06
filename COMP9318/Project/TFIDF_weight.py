import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer

from Project import helper

ins = helper.strategy()
vectorizer = TfidfVectorizer(stop_words='english', preprocessor=None, max_features=210)
class0words = ' '.join(list(map(lambda x: ' '.join(x), ins.class0)))
class1words = ' '.join(list(map(lambda x: ' '.join(x), ins.class1)))
tfidf = vectorizer.fit_transform([class0words, class1words])
word = vectorizer.get_feature_names()
weight = tfidf.toarray()
stat = defaultdict(lambda: [0, 0,0])  # format: dictionary[word] = [class0weight,class1weight,class0/class1]
for i in range(len(weight)):
    print(f'-----class {i} -----')
    for j in range(len(word)):
        stat[word[j]][i] = weight[i][j]
        print(f'{word[j]}:{weight[i][j]}', end='\t')
    print()
for e in stat:
    stat[e][2] = stat[e][0]/stat[e][1]
sortedFreq = sorted(stat.items(), key=lambda x: x[1][2],
             reverse=True)  # class0weight - class1weight, if rev: class0weight bigger
print(sortedFreq)


