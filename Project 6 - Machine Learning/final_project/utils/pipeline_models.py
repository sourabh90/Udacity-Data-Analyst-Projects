#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 9 23:57:43 2017

@author: sourabh
"""

from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import recall_score, make_scorer


def pipeline_SVC_model(features_train, labels_train, features_test, labels_test):
    from sklearn.svm import SVC
    
    estimators = [('feature_transformer', MinMaxScaler()),
                  ('selection', SelectKBest()),
                  ('reduce_dim', PCA()), 
                  ('clf', SVC())
                 ]
    
    param_grid = {'selection__k': [5, 7, 9, 10, 'all'],
                  'clf__C': [0.01, 0.1, 1, 10, 100, 1000, 10000],
                  'reduce_dim__n_components': [1, 2, 3, 4, 5],
                  'reduce_dim__whiten': [True, False]
                  }
    
    pipeline = Pipeline(estimators)
    grid_search = GridSearchCV(pipeline, param_grid=param_grid, 
                               n_jobs=-1, scoring='recall', cv=15)
    grid_search.fit(features_train, labels_train)
    return grid_search


def pipeline_LSVC_model(features_train, labels_train, features_test, labels_test):
    from sklearn.svm import LinearSVC
    
    estimators = [('feature_transformer', MinMaxScaler()),
                  ('selection', SelectKBest()),
                  ('reduce_dim', PCA()), 
                  ('clf', LinearSVC())
                 ]
    
    param_grid = {'selection__k': [5, 7, 9, 10, 'all'],
                  'clf__C': [0.001, 0.01, 0.1, 1, 10, 100],
                  'reduce_dim__n_components': [1, 2, 3, 4, 5],
                  'reduce_dim__whiten': [True, False]
                  }
    
    pipeline = Pipeline(estimators)
    grid_search = GridSearchCV(pipeline, param_grid=param_grid, 
                               n_jobs=-1, scoring='recall', cv=15)
    grid_search.fit(features_train, labels_train)
    return grid_search    
    
    
#def pipeline_KNN_model(features_train, labels_train, features_test, labels_test, cv):
def pipeline_KNN_model(features, labels, cv):
    from time import time
    from sklearn.neighbors import KNeighborsClassifier
    
    start = time()

    estimators = [('feature_transformer', MinMaxScaler()),
                  ('reduce_dim', PCA()), 
                  ('clf', KNeighborsClassifier())
                 ]
    
    param_grid = {'clf__n_neighbors': [1, 2, 3, 4, 5, 8, 10],
                  'clf__algorithm': ['ball_tree', 'kd_tree'],
                  'clf__leaf_size': [1, 2, 3, 4, 5, 10],
                  'reduce_dim__n_components': [3, 4, 5, 6, 7, 8]
                  }
    
    pipeline = Pipeline(estimators)
    grid_search = GridSearchCV(pipeline, param_grid=param_grid,
                               scoring = 'recall',
                               n_jobs=-1, cv=cv
                               )
    grid_search.fit(features, labels)
    
    print '\nTime taken to Grid Search KNN model : {} sec'.format(round(time() - start, 2))
    
    return grid_search
    
    
def pipeline_DT_model(features_train, labels_train, features_test, labels_test):
    from sklearn.tree import DecisionTreeClassifier
    
    estimators = [('feature_transformer', MinMaxScaler()),
                  ('selection', SelectKBest()),
                  ('reduce_dim', PCA()), 
                  ('clf', DecisionTreeClassifier())
                 ]
    
    param_grid = {'selection__k': [5, 7, 9, 10, 'all'],
                  'reduce_dim__n_components': [1, 2, 3, 4, 5]
                  }
    
    pipeline = Pipeline(estimators)
    grid_search = GridSearchCV(pipeline, param_grid=param_grid, cv = 15)
    grid_search.fit(features_train, labels_train)
    
    print "DT Best Model Score : ", grid_search.score(features_test, labels_test)
    return grid_search   
    
    
def pipeline_RF_model(features_train, labels_train, features_test, labels_test):
    from time import time
    from scipy.stats import randint as sp_randint
    from sklearn.model_selection import RandomizedSearchCV
    from sklearn.ensemble import RandomForestClassifier
    
    start = time()
    clf = RandomForestClassifier(n_estimators=20, random_state=42, n_jobs=-1)
    
    # specify parameters and distributions to sample from
    param_dist = {"max_depth": [3, None],
                  "max_features": sp_randint(1, 11),
                  "min_samples_split": sp_randint(2, 11),
                  "min_samples_leaf": sp_randint(1, 11),
                  "bootstrap": [True, False],
                  "criterion": ["gini", "entropy"]}
    
    random_search = RandomizedSearchCV(clf, param_distributions=param_dist,
                               #scoring=make_scorer(recall_score), 
                               n_iter=20,
                               n_jobs=-1)
    random_search.fit(features_train, labels_train)
    
    print '\nTime taken to Random Search RF model : {} sec'.format(round(time() - start, 2))
    
    return random_search    
    
    
def pipeline_LRegr_model(features, labels, cv):
    from time import time
    from sklearn.linear_model import LogisticRegression
    
    start = time()
    
    estimators = [('feature_transformer', MinMaxScaler()),
                  ('selection', SelectKBest()),
                  ('reduce_dim', PCA()),
                  ('clf', LogisticRegression())
                               ]
    
    param_grid = {'selection__k': [5, 6, 7, 8, 'all'],
                  'clf__C': [1e-2, 1e-1, 1, 2, 5, 10],
                  'clf__class_weight': [{True: 12, False: 1},
                                               {True: 10, False: 1},
                                               {True: 8, False: 1}],
                  'clf__tol': [1e-1, 1e-4, 1e-16,
                                      1e-64, 1e-256],
                  'reduce_dim__n_components': [2, 3, 4]#,
                  #'reduce_dim__whiten': [True, False]
                  }
    
    pipeline = Pipeline(estimators)
    grid_search = GridSearchCV(pipeline, param_grid=param_grid,
                               scoring = 'recall',
                               n_jobs=-1, cv=cv
                               )
    grid_search.fit(features, labels)
    print '\nTime taken to Grid Search Logistics Regression model : {} sec'.format(round(time() - start, 2))
    
    return grid_search        

    