# code for question 4

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.feature_selection import SelectKBest, chi2

df_trte = pd.read_csv('snippets_all.csv')
df_tr = pd.read_csv('snippets_train.csv')
df_te = pd.read_csv('snippets_test.csv')

# set up the vocabulary (the global set of "words" or tokens) for training and test datasets
vectorizer = CountVectorizer()
vectorizer.fit(df_trte.snippet)
# print(vectorizer.get_feature_names())

# apply this vocabulary to transform the text snippets to vectors of word counts
X_train = vectorizer.transform(df_tr.snippet)
X_test = vectorizer.transform(df_te.snippet)
y_train = df_tr.section
y_test = df_te.section
print(X_train)
print(y_train[0])

# Debugging
# print("X train: ", X_train.shape)
# print("X test: ", X_test.shape)
# print("Y train: ", y_train.shape)
# print("Y test: ", y_test.shape)

# learn a Naive Bayes classifier on the training set
clf = MultinomialNB(alpha=0.5)
MultinomialNB(alpha=0.5, class_prior=None, fit_prior=True)
clf.fit(X_train, y_train)
pred_train = clf.predict(X_train)
score_train = metrics.accuracy_score(y_train, pred_train)
pred_test = clf.predict(X_test)
score_test = metrics.accuracy_score(y_test, pred_test)
print("Train/test accuracy using all features: ", score_train, score_test)


# Use Chi^2 to select top 10000 features
ch2_10000 = SelectKBest(chi2, k=10000)
ch2_10000.fit(X_train, y_train)
# Project training data onto top 10000 selected features
X_train_kbest_10000 = ch2_10000.transform(X_train)
# Train NB Classifier using top 10 selected features
clf_kbest_10000 = MultinomialNB(alpha=0.5, class_prior=None, fit_prior=True)
clf_kbest_10000.fit(X_train_kbest_10000,y_train)
# Predictive accuracy on training set
pred_train_kbest_10000 = clf_kbest_10000.predict(X_train_kbest_10000)
score_train_kbest_10000 = metrics.accuracy_score(y_train,pred_train_kbest_10000)
# Project test data onto top 10000 selected features
X_test_kbest_10000 = ch2_10000.transform(X_test)
# Predictive accuracy on test set
pred_test_kbest_10000 = clf_kbest_10000.predict(X_test_kbest_10000)
score_test_kbest_10000 = metrics.accuracy_score(y_test,pred_test_kbest_10000)
print("Train/test accuracy for top 10K features", score_train_kbest_10000, score_test_kbest_10000)

# Use Chi^2 to select top 1000 features
ch2_1000 = SelectKBest(chi2, k=1000)
ch2_1000.fit(X_train, y_train)
# Project training data onto top 1000 selected features
X_train_kbest_1000 = ch2_1000.transform(X_train)
# Train NB Classifier using top 1000 selected features
clf_kbest_1000 = MultinomialNB(alpha=0.5, class_prior=None, fit_prior=True)
clf_kbest_1000.fit(X_train_kbest_1000,y_train)
# Predictive accuracy on training set
pred_train_kbest_1000 = clf_kbest_1000.predict(X_train_kbest_1000)
score_train_kbest_1000 = metrics.accuracy_score(y_train,pred_train_kbest_1000)
# Project test data onto top 1000 selected features
X_test_kbest_1000 = ch2_1000.transform(X_test)
# Predictive accuracy on test set
pred_test_kbest_1000 = clf_kbest_1000.predict(X_test_kbest_1000)
score_test_kbest_1000 = metrics.accuracy_score(y_test,pred_test_kbest_1000)
print("Train/test accuracy for top 1K features", score_train_kbest_1000, score_test_kbest_1000)

# Use Chi^2 to select top 100 features
ch2_100 = SelectKBest(chi2, k=100)
ch2_100.fit(X_train, y_train)
# Project training data onto top 100 selected features
X_train_kbest_100 = ch2_100.transform(X_train)
# Train NB Classifier using top 100 selected features
clf_kbest_100 = MultinomialNB(alpha=0.5, class_prior=None, fit_prior=True)
clf_kbest_100.fit(X_train_kbest_100,y_train)
# Predictive accuracy on training set
pred_train_kbest_100 = clf_kbest_100.predict(X_train_kbest_100)
score_train_kbest_100 = metrics.accuracy_score(y_train,pred_train_kbest_100)
# Project test data onto top 100 selected features
X_test_kbest_100 = ch2_100.transform(X_test)
# Predictive accuracy on test set
pred_test_kbest_100 = clf_kbest_100.predict(X_test_kbest_100)
score_test_kbest_100 = metrics.accuracy_score(y_test,pred_test_kbest_100)
print("Train/test accuracy for top 100 features", score_train_kbest_100, score_test_kbest_100)

# Use Chi^2 to select top 10 features
ch2_10 = SelectKBest(chi2, k=10)
ch2_10.fit(X_train, y_train)
# Project training data onto top 10 selected features
X_train_kbest_10 = ch2_10.transform(X_train)
# Train NB Classifier using top 10 selected features
clf_kbest_10 = MultinomialNB(alpha=0.5, class_prior=None, fit_prior=True)
clf_kbest_10.fit(X_train_kbest_10,y_train)
# Predictive accuracy on training set
pred_train_kbest_10 = clf_kbest_10.predict(X_train_kbest_10)
score_train_kbest_10 = metrics.accuracy_score(y_train,pred_train_kbest_10)
# Project test data onto top 10 selected features
X_test_kbest_10 = ch2_10.transform(X_test)
# Predictive accuracy on test set
pred_test_kbest_10 = clf_kbest_10.predict(X_test_kbest_10)
score_test_kbest_10 = metrics.accuracy_score(y_test,pred_test_kbest_10)
print("Train/test accuracy for top 10 features", score_train_kbest_10, score_test_kbest_10)

