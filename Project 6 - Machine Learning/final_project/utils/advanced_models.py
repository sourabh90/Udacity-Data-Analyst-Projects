#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 22:18:27 2017

@author: sourabh
"""
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import cross_val_score


def rf_model(features_train, labels_train, features_test, labels_test):
    clf = RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=-1)
    clf.fit(features_train, labels_train)
    print "Random Forest Classifier Score : ", clf.score(features_test, labels_test)
    return clf

    
def ET_model(features_train, labels_train, features_test, labels_test):
    clf = ExtraTreesClassifier(n_estimators=100, criterion='gini',
                                  max_features=0.1,min_samples_split=10, 
                                  min_samples_leaf=2,random_state=42)
    clf.fit(features_train, labels_train)
    scores = cross_val_score(clf, features_train, labels_train)
    print "Extra Tree Classifier Score : ", scores.mean()
    return clf

    
def ET_feature_importances(clf, selected_features):
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    print "Feature ranking for ET Classifier:"
    
    for f in range(len(selected_features)-1):
        print "%d. feature %s (%f)" % (f + 1, selected_features[indices[f]], importances[indices[f]])

    
def bagging_classifer(features_train, labels_train, features_test, labels_test):
    bagging = BaggingClassifier(KNeighborsClassifier(
                                        n_neighbors=1, algorithm='auto',
                                        weights='uniform', n_jobs=-1,
                                        leaf_size=2, metric='minkowski'
                                                     ), 
                                max_samples=0.5, max_features=0.5)
    bagging.fit(features_train, labels_train)
    print "Bagging Score : ", bagging.score(features_test, labels_test)
    return bagging
    
    
def ada_boost_classifer(features_train, labels_train, features_test, labels_test):
    clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=3), n_estimators=70)
    clf.fit(features_train, labels_train)
    print "Bagging Score : ", clf.score(features_test, labels_test)
    return clf
    