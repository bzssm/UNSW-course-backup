# code for question 2

import arff, numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from sklearn import tree
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import sys
import warnings

# fixed random seed
np.random.seed(1)

def warn(*args, **kwargs):
    pass

def label_enc(labels):
    le = preprocessing.LabelEncoder()
    le.fit(labels)
    return le

def features_encoders(features,categorical_features='all'):
    n_samples, n_features = features.shape
    label_encoders = [preprocessing.LabelEncoder() for _ in range(n_features)]

    X_int = np.zeros_like(features, dtype=np.int)

    for i in range(n_features):
        feature_i = features[:, i]
        label_encoders[i].fit(feature_i)
        X_int[:, i] = label_encoders[i].transform(feature_i)
        
    enc = preprocessing.OneHotEncoder(categorical_features=categorical_features)
    return enc.fit(X_int),label_encoders

def feature_transform(features,label_encoders, one_hot_encoder):
    
    n_samples, n_features = features.shape
    X_int = np.zeros_like(features, dtype=np.int)
    
    for i in range(n_features):
        feature_i = features[:, i]
        X_int[:, i] = label_encoders[i].transform(feature_i)

    return one_hot_encoder.transform(X_int).toarray()

warnings.warn = warn

class DataFrameImputer(TransformerMixin):

    def fit(self, X, y=None):

        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
            index=X.columns)

        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)


def load_data(path):
    dataset = arff.load(open(path, 'r'))
    data = np.array(dataset['data'])
    data = pd.DataFrame(data)
    data = DataFrameImputer().fit_transform(data).values
    attr = dataset['attributes']

    # mask categorical features
    masks = []
    for i in range(len(attr)-1):
        if attr[i][1] != 'REAL':
            masks.append(i)
    return data, masks

def preprocess(data,masks, noise_ratio):
    # split data
    train_data, test_data = train_test_split(data,test_size=0.3,random_state=0)

    # test data
    test_features = test_data[:,0:test_data.shape[1]-1]
    test_labels = test_data[:,test_data.shape[1]-1]

    # training data
    features = train_data[:,0:train_data.shape[1]-1]
    labels = train_data[:,train_data.shape[1]-1]

    classes = list(set(labels))
    # categorical features need to be encoded
    if len(masks):
        one_hot_enc, label_encs = features_encoders(data[:,0:data.shape[1]-1],masks)
        test_features = feature_transform(test_features,label_encs,one_hot_enc)
        features = feature_transform(features,label_encs,one_hot_enc)

    le = label_enc(data[:,data.shape[1]-1])
    labels = le.transform(train_data[:,train_data.shape[1]-1])
    test_labels = le.transform(test_data[:,test_data.shape[1]-1])
    
    # add noise
    np.random.seed(1234)
    noise = np.random.randint(len(classes)-1, size=int(len(labels)*noise_ratio))+1
    
    noise = np.concatenate((noise,np.zeros(len(labels) - len(noise),dtype=np.int)))
    labels = (labels + noise) % len(classes)

    return features,labels,test_features,test_labels

# load data
paths = ['balance-scale','primary-tumor',
         'glass','heart-h']
noise = [0,0.2,0.5,0.8]

scores = []
params = []

for path in paths:
    score = []
    param = []
    path += '.arff'
    data, masks = load_data(path)
    
    # training on data with %50 noise and default parameters
    features, labels, test_features, test_labels = preprocess(data, masks, 0.5)
    tree = DecisionTreeClassifier(random_state=0,min_samples_leaf=2, min_impurity_decrease=0)
    tree.fit(features, labels)
    tree_preds = tree.predict(test_features)
    tree_performance = accuracy_score(test_labels, tree_preds)
    score.append(tree_performance)
    param.append(tree.get_params()['min_samples_leaf'])
    
    # training on data with noise %0, %20, %50, %80
    for noise_ratio in noise:
        features, labels, test_features, test_labels = preprocess(data, masks, noise_ratio)
        param_grid = {'min_samples_leaf': np.arange(2,30,5)}

        grid_tree = GridSearchCV(DecisionTreeClassifier(random_state=0), param_grid,cv=10,return_train_score=True)
        grid_tree.fit(features, labels)

        estimator = grid_tree.best_estimator_
        tree_preds = grid_tree.predict(test_features)
        tree_performance = accuracy_score(test_labels, tree_preds)
        score.append(tree_performance)
        param.append(estimator.get_params()['min_samples_leaf'])

    scores.append(score)
    params.append(param)

# print the results
header = "{:^123}".format("Decision Tree Results") + '\n' + '-' * 123  + '\n' + \
"{:^15} | {:^16} | {:^16} | {:^16} | {:^16} | {:^16} |".format("Dataset", "Default", "0%", "20%", "50%", "80%")


# print result table
print(header)
for i in range(len(scores)):
    #scores = score_list[i][1]
    print("{:<16}".format(paths[i]),end="")
    for j in range(len(params[i])):
        print("|  {:>6.2%} ({:>2})     " .format(scores[i][j],params[i][j]),end="")
    print('|\n')
print('\n')