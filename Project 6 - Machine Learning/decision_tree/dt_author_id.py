#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 3 (decision tree) mini-project.

    Use a Decision Tree to identify emails from the Enron corpus by author:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
from sklearn import tree

sys.path.append("../tools/")
from email_preprocess import preprocess

def custom_print(string):
	print '\x1b[0;31;42m{0}\x1b[0m'.format(string)

### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
start = time()
features_train, features_test, labels_train, labels_test = preprocess()
print "Data processing time : {} sec".format(round(time() - start, 2))

custom_print("Number of features : {0}".format(len(features_train[0])))

#########################################################
### your code goes here ###
clf = tree.DecisionTreeClassifier(min_samples_split = 40)

start = time()
clf.fit(features_train, labels_train)
print "Model training time : {} sec".format(round(time() - start, 2))

start = time()
clf.predict(features_test)
print "Model prediction time : {} sec".format(round(time() - start, 2))

custom_print("Accuracy :: {0}".format(clf.score(features_test, labels_test)))
#########################################################


