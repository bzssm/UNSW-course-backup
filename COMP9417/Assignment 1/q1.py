# code for question 1

import arff
import numpy as np
from itertools import product
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_score, KFold
from sklearn.utils import resample
from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from scipy.stats import ttest_ind

seeds = [2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37]
score_list = []

for fname in ["anneal.arff", "audiology.arff", "autos.arff", "credit-a.arff", \
              "hypothyroid.arff", "letter.arff", "microarray.arff", "vote.arff"]:
    dataset = arff.load(open(fname), 'r')
    data = np.array(dataset['data'])

    X = np.array(data)[:, :-1]
    Y = np.array(data)[:, -1]

    # turn unknown/none/? into a separate value
    for i, j in product(range(len(data)), range(len(data[0]) - 1)):
        if X[i, j] is None:
            X[i, j] = len(dataset['attributes'][j][1])

    # a hack to turn negative categories positive for autos.arff
    for i in range(Y.shape[0]):
        if Y[i] < 0:
            Y[i] += 7

    # identify and extract categorical/non-categorical features
    categorical, non_categorical = [], []
    for i in range(len(dataset['attributes']) - 1):
        if isinstance(dataset['attributes'][i][1], str):
            non_categorical.append(X[:, i])
        else:
            categorical.append(X[:, i])

    categorical = np.array(categorical).T
    non_categorical = np.array(non_categorical).T

    if categorical.shape[0] == 0:
        transformed_X = non_categorical
    else:
        # encode categorical features
        encoder = OneHotEncoder(n_values = 'auto',
                                categorical_features = 'all',
                                dtype = np.int32,
                                sparse = False,
                                handle_unknown = 'error')
        encoder.fit(categorical)
        categorical = encoder.transform(categorical)
        if non_categorical.shape[0] == 0:
            transformed_X = categorical
        else:
            transformed_X = np.concatenate((categorical, non_categorical), axis = 1)

    # concatenate the feature array and the labels for resampling purpose
    Y = np.array([Y], dtype = np.int)
    input_data = np.concatenate((transformed_X, Y.T), axis = 1)

    # build the models
    models = [DummyClassifier(strategy = 'most_frequent')] \
              + [KNeighborsClassifier(n_neighbors = 1, algorithm = "brute")] * 5 \
              + [DecisionTreeClassifier()] * 5

    # resample and run cross validation
    portion = [1.0, 0.1, 0.25, 0.5, 0.75, 1.0, 0.1, 0.25, 0.5, 0.75, 1.0]
    sample, scores = [None] * 11, [None] * 11
    for i in range(11):
        sample[i] = resample(input_data,
                             replace = False,
                             n_samples = int(portion[i] * input_data.shape[0]),
                             random_state = seeds[i])
        score = [None] * 10
        for j in range(10):
            score[j] = np.mean(cross_val_score(models[i],
                                               sample[i][:, :-1],
                                               sample[i][:, -1].astype(np.int),
                                               scoring = 'accuracy',
                                               cv = KFold(10, True, seeds[j])))
        scores[i] = score

    score_list.append((fname[:-5], 1 - np.array(scores)))

# print the results
header = ["{:^123}".format("Nearest Neighbour Results") + '\n' + '-' * 123  + '\n' + \
          "{:^15} | {:^10} | {:^16} | {:^16} | {:^16} | {:^16} | {:^16}" \
          .format("Dataset", "Baseline", "10%", "25%", "50%", "75%", "100%"),
          "{:^123}".format("Decision Tree Results") + '\n' + '-' * 123  + '\n' + \
          "{:^15} | {:^10} | {:^16} | {:^16} | {:^16} | {:^16} | {:^16}" \
          .format("Dataset", "Baseline", "10%", "25%", "50%", "75%", "100%")]
offset = [1, 6]

for k in range(2):
    print(header[k])
    for i in range(8):
        scores = score_list[i][1]
        p_value = [None] * 5
        for j in range(5):
            _, p_value[j] = ttest_ind(scores[0], scores[j + offset[k]], equal_var = False)

        print("{:<15} | {:>10.2%}".format(score_list[i][0], np.mean(scores[0])), end = '')
        for j in range(5):
            print(" | {:>6.2%} ({:>5.2%}) {}" .format(np.mean(scores[j + offset[k]]),
                                                      np.std(scores[j + offset[k]]),
                                                      '*' if p_value[j] < 0.05 else ' '), end = '')
        print()
    print()

with open('q1n.txt','w') as f:
    errs = np.mean([(np.mean(score_list[i][1][0])-np.mean(score_list[i][1][1]))/np.mean(score_list[i][1][0])*100 for i in range(8)])
    f.write(f'{errs:.2f}\n')
    errs = np.mean([(np.mean(score_list[i][1][0])-np.mean(score_list[i][1][5]))/np.mean(score_list[i][1][0])*100 for i in range(8)])
    f.write(f'{errs:.2f}\n')
    errs = np.mean([(np.mean(score_list[i][1][0])-np.mean(score_list[i][1][6]))/np.mean(score_list[i][1][0])*100 for i in range(8)])
    f.write(f'{errs:.2f}\n')
    errs = np.mean([(np.mean(score_list[i][1][0])-np.mean(score_list[i][1][10]))/np.mean(score_list[i][1][0])*100 for i in range(8)])
    f.write(f'{errs:.2f}\n')