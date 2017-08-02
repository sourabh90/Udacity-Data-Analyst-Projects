#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
import numpy as np
from time import time
from sklearn import svm

sys.path.append("../tools/")
from email_preprocess import preprocess


def custom_print(string):
	"""Prints the string in a color coded format"""
	print '\x1b[0;31;42m{0}\x1b[0m'.format(string)


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
start = time()
features_train, features_test, labels_train, labels_test = preprocess()
custom_print("Time Taken for setting up data :: {0} secs".format(round(time() - start)))

#########################################################
### your code goes here ###

# Use 1% of the data to speed up the model learning 
features_train = features_train[:len(features_train)/100] 
labels_train = labels_train[:len(labels_train)/100] 


start = time()

# SVC Linear classifier 
clf = svm.SVC(C=10000.0)

# Fit the classifier 
clf.fit(features_train, labels_train)

custom_print("Time Taken for training the SVM classifier :: {0} secs\n\n{1}".format(round(time() - start), clf))

# Predict on the test set
start = time()
answer = clf.predict(features_test)
custom_print(answer)

custom_print("Time taken for prediction : {} sec".format(round(time() - start, 2)))

# Accuracy of the classifier
custom_print(clf.score(features_test, labels_test))
#########################################################

# Print 10th, 26th, 50th prediction data point
custom_print("10th : {0}\n26th : {1}\n50th : {2}".format(answer[10], answer[26], answer[50]))

# How many predicted Chris -- class 1
custom_print("Total Prediction for chris (class 1) : {}".format(np.sum(answer)))

