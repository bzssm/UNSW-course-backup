import helper
import itertools
from collections import defaultdict
import numpy as np


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


def fool_classifier(test_data):  ## Please do not change the function defination...
    ## Read the test data file, i.e., 'test_data.txt' from Present Working Directory...

    ## You are supposed to use pre-defined class: 'strategy()' in the file `helper.py` for model trainin    g (if any),
    #  and modifications limit checkin
    strategy_instance = helper.strategy()
    parameters = {}
    # initial parameters
    parameters['gamma'] = 'auto'
    parameters['C'] = 100
    parameters['kernel'] = 'linear'
    parameters['degree'] = 3
    parameters['coef0'] = 0.0
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_extraction.text import CountVectorizer
    for i in range(150, 450, 5):
        vectorizer = CountVectorizer(stop_words='english', min_df=10, preprocessor=None, max_features=i)
        try:
            vectorizer.fit(merge(['class-0.txt', 'class-1.txt']))
        except Exception:
            continue
        X_train = vectorizer.transform(merge(['class-0.txt', 'class-1.txt']))
        X_test = vectorizer.transform(open('test_data.txt', 'r'))
        Y_train = ['class-0'] * 360 + ['class-1'] * 180
        Y_test = ['class-1'] * 200
        # print(X_train.shape)
        # print(vectorizer.get_feature_names())
        clf = strategy_instance.train_svm(parameters, X_train, Y_train)
        # print(clf.predict(X_test))
        print('c = ', 100, 'mindf = ', 10, 'i = ', i, end='')
        print(correctrate(clf.predict(X_test), Y_test), correctrate(clf.predict(X_train), Y_train))
        # print(X_train)

    ##..................................#
    #
    #
    #
    ## Your implementation goes here....#
    #
    #
    #
    ##..................................#

    ## Write out the modified file, i.e., 'modified_data.txt' in Present Working Directory...

    ## You can check that the modified text is within the modification limits.
    # modified_data='./modified_data.txt'
    # assert strategy_instance.check_data(test_data, modified_data)
    return strategy_instance  ## NOTE: You are required to return the instance of this class.


def init_matirx(set_key_list):
    '''建立矩阵，矩阵的高度和宽度为关键词集合的长度+1'''
    edge = len(set_key_list) + 1
    # matrix = np.zeros((edge, edge), dtype=str)
    matrix = [['' for j in range(edge)] for i in range(edge)]
    return matrix


def build_matrix(vocab):
    '''初始化矩阵，将关键词集合赋值给第一列和第二列'''
    reverse_vocab = dict(zip(vocab.values(), vocab.keys()))
    keys = list(vocab.keys())
    matrix = init_matirx(keys)
    for v in vocab.values():
        matrix[0][v + 1] = reverse_vocab[v]
    matrix = list(map(list, zip(*matrix)))
    # matrix[0][1:] = np.array(keys)
    for v in vocab.values():
        matrix[0][v + 1] = reverse_vocab[v]
    return matrix


def show_matrix(matrix):
    matrixtxt = ''
    count = 0
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            matrixtxt = matrixtxt + str(matrix[i][j]) + '\t'
        matrixtxt = matrixtxt[:-1] + '\n'
        count = count + 1
        # print('No.'+str(count)+' had been done!')
    return matrixtxt


def count_matrix(matrix, formated_data):
    ''' 计算各个关键词共现次数 '''
    for row in range(1, len(matrix)):
        # 遍历矩阵第一行，跳过下标为0的元素
        for col in range(1, len(matrix)):
            # 遍历矩阵第一列，跳过下标为0的元素
            # 实际上就是为了跳过matrix中下标为[0][0]的元素，因为[0][0]为空，不为关键词
            if matrix[0][row] == matrix[col][0]:
                # 如果取出的行关键词和取出的列关键词相同，则其对应的共现次数为0，即矩阵对角线为0
                matrix[col][row] = str(0)
            else:
                counter = 0
                # 初始化计数器
                for ech in formated_data:
                    # 遍历格式化后的原始数据，让取出的行关键词和取出的列关键词进行组合，
                    # 再放到每条原始数据中查询
                    if matrix[0][row] in ech and matrix[col][0] in ech:
                        counter += 1
                    else:
                        continue
                matrix[col][row] = str(counter)
    return matrix


def fool(test_data):  ## Please do not change the function defination...
    ## Read the test data file, i.e., 'test_data.txt' from Present Working Directory...

    ## You are supposed to use pre-defined class: 'strategy()' in the file `helper.py` for model trainin    g (if any),
    #  and modifications limit checkin
    strategy_instance = helper.strategy()
    parameters = {}
    # initial parameters
    parameters['gamma'] = 'auto'
    parameters['C'] = 100
    parameters['kernel'] = 'linear'
    parameters['degree'] = 3
    parameters['coef0'] = 0.0
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer(stop_words='english', min_df=10, preprocessor=None, max_features=210)

    corpus = merge(['class-0.txt', 'class-1.txt'])
    vectorizer.fit(corpus)

    X_train = vectorizer.transform(merge(['class-0.txt', 'class-1.txt']))
    X_test = vectorizer.transform(open('test_data.txt', 'r'))
    Y_train = ['class-0'] * 360 + ['class-1'] * 180
    Y_test = ['class-1'] * 200
    # print(X_train.shape)
    # print(vectorizer.get_feature_names())
    clf = strategy_instance.train_svm(parameters, X_train, Y_train)
    # print(clf.predict(X_test))
    print('c = ', 100, 'mindf = ', 10, 'i = ', 210, end='')
    print(correctrate(clf.predict(X_test), Y_test), correctrate(clf.predict(X_train), Y_train))

    # cal keyword w.r.t class 0 and class 1
    vocab = vectorizer.vocabulary_
    print('size of vocab={}\n vocab={}'.format(len(vocab), vocab))
    kw0 = defaultdict(lambda: 0)
    kw1 = defaultdict(lambda: 0)

    # feature_0 = vectorizer.inverse_transform(X_train[:360])
    # feature_1 = vectorizer.inverse_transform(X_train[361:])
    # for f in feature_0:
    #     print(f)
    # print('>>> class-1')
    # for f in feature_1:
    #     print(f)
    # for f in feature_0:
    #     kw0 +=list(f)

    # for f in feature_1:
    #     kw1 +=list(f)

    # kw0 = set(kw0)
    # kw1 = set(kw1)
    # overlap = kw0 & kw1

    # cal keyword-frequency w.r.t class - and class 1
    for item in strategy_instance.class0:
        for w in item:
            if w in vocab.keys():
                kw0[w] += 1

    kw0 = dict(sorted(kw0.items(), key=lambda item: item[1], reverse=True))
    # print(kw0)
    for item in strategy_instance.class1:
        for w in item:
            if w in vocab.keys():
                kw1[w] += 1
    kw1 = dict(sorted(kw1.items(), key=lambda item: item[1], reverse=True))
    # print(kw1)
    overlap = set(kw0.keys()) & set(kw1.keys())
    print('class-0={}, class-1={}, overlap={}'.format(len(kw0), len(kw1), len(overlap)))

    # construction co-occur matrix
    matrix0 = build_matrix(vocab)
    matrix1 = build_matrix(vocab)
    # print(show_matrix(matrix))

    co_matrix0 = count_matrix(matrix0, strategy_instance.class0)
    co_matrix1 = count_matrix(matrix1, strategy_instance.class1)

    print('>>> class 0')
    print(show_matrix(co_matrix0))
    print('>>> class 1')
    print(show_matrix(co_matrix1))

    example0 = strategy_instance.class0[0]
    example1 = strategy_instance.class1[0]
    print('example0={}\nexample1={}'.format(example0, example1))
    word_set = set(example0 + example1) & set(vocab)
    print(word_set)
    for w in word_set:
        print('0: ', w, co_matrix0[vocab[w] + 1])
        print('1: ', w, co_matrix1[vocab[w] + 1])


if __name__ == '__main__':
    fool('test_data.txt')
