from collections import OrderedDict
import helper
import itertools


def merge(filelist):
    res = []
    for file in filelist:
        with open(file, 'r') as f:
            for line in f:
                if line:
                    res.append(line)
    return res


def correctrate(predict, fact):
    if len(predict) != len(fact):
        print('false matrix')
        return
    correct = 0
    for i in range(len(predict)):
        if predict[i] == fact[i]:
            correct += 1
    return (correct, len(predict), correct / len(predict))


def fool_classifier(test_data):
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
    # from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = TfidfVectorizer(binary=True)  # ,min_df=2,max_df=0.8,max_features=240)
    # vectorizer.fit(f)
    X_train = vectorizer.fit_transform(f)
    # X_test = vectorizer.transform(open('modified_data.txt', 'r'))
    Y_train = ['class-0'] * 360 + ['class-1'] * 180
    # Y_test = ['class-0'] * 200
    clf = strategy_instance.train_svm(parameters, X_train, Y_train)
    # print(clf.coef_.shape)
    # print(len(vectorizer.vocabulary_))

    # words = vectorizer.vocabulary_.keys()
    words_index = dict([e[::-1] for e in vectorizer.vocabulary_.items()])
    coef = list(clf.coef_.toarray().tolist()[0])
    # print(coef)
    words_coef = {}
    for i in words_index:
        words_coef[words_index[i]] = coef[i]

    print(sorted(words_coef.items(),key=lambda x:x[1],reverse=True))
    words_postion = OrderedDict(
        zip([e[0] for e in sorted(words_coef.items(), key=lambda x: x[1])], itertools.count(0)))

    print(words_postion)
    # print(words_postion)


    with open('test_data.txt', 'r') as tf:
        with open('modified_data.txt', 'w') as mf:
            for line in tf:
                line_copy = line.strip().split()
                words_to_delete = set()
                for word in line_copy:
                    if word in words_coef:
                        if words_coef[word]>0:
                            words_to_delete.add(word)
                if len(words_to_delete)>20:
                    words_to_delete_eval = {}
                    for word in words_to_delete:
                        words_to_delete_eval[word] = words_postion[word]
                    words_to_delete = set(dict(sorted(words_to_delete_eval.items(),key=lambda x:x[1])[-20:]).keys())
                    for i in range(len(line_copy)):
                        if line_copy[i] in words_to_delete:
                            line_copy[i] = ''
                    mf.write(' '.join([e for e in line_copy if e]))
                    mf.write('\n')
                else:
                    words_to_add = set()
                    for word in words_postion:
                        if len(words_to_add) == 20-len(words_to_delete):
                            break
                        if word not in words_to_delete and word not in line_copy:
                            words_to_add.add(word)
                    for i in range(len(line_copy)):
                        if line_copy[i] in words_to_delete:
                            line_copy[i] = ''
                    line_copy.extend(words_to_add)
                    mf.write(' '.join([e for e in line_copy if e]))
                    mf.write('\n')
    # strategy_instance.check_data('test_data.txt', 'modified_data.txt')
    # print(accuracy_score(Y_test, clf.predict(X_test)))

    return strategy_instance  ## NOTE: You are required to return the instance of this class.


fool_classifier('test_data.txt')
