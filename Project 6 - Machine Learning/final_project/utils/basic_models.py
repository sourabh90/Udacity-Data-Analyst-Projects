#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 01:08:52 2017

@author: sourabh
"""

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


def naive_bayes_model(features_train, labels_train, features_test, labels_test):
    clf = GaussianNB()
    clf.fit(features_train, labels_train)
    print "Gaussian Naive Bayes Score : ", clf.score(features_test, labels_test)
    return clf

def svm_model(features_train, labels_train, features_test, labels_test):
    clf = SVC()
    clf.fit(features_train, labels_train)
    print "Support Vector model Score : ", clf.score(features_test, labels_test)
    return clf
    
def decision_tree_model(features_train, labels_train, features_test, labels_test):
    clf = DecisionTreeClassifier()
    clf.fit(features_train, labels_train)
    print "Decision Tree model Score : ", clf.score(features_test, labels_test)
    return clf

def KNN_model(features_train, labels_train, features_test, labels_test):
    clf = KNeighborsClassifier()
    clf.fit(features_train, labels_train)
    print "K Nearest Nerighbor model Score : ", clf.score(features_test, labels_test)
    return clf    
    