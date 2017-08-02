#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 1 (Naive Bayes) mini-project. 

    Use a Naive Bayes Classifier to identify emails by their authors
    
    authors and labels:
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn.naive_bayes import GaussianNB

### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
start = time()
features_train, features_test, labels_train, labels_test = preprocess()
print "Data processing time : {} sec".format(round(time() - start, 2))

#########################################################
### your code goes here ###

# Gaussian Naive Bayes Classifier
clf = GaussianNB()

start = time()
# Fit the classifier for train data
clf.fit(features_train, labels_train)

print "Time taken for learning : {} sec".format(round(time() - start, 2))


# Predict on the test set
start = time()
print clf.predict(features_test)

print "Time taken for prediction : {} sec".format(round(time() - start, 2))
#########################################################

# Accuracy of the classifier
print clf.score(features_test, labels_test)


