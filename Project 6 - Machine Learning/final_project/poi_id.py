#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 9 23:57:43 2017

@author: sourabh
"""

import sys
import pickle
sys.path.append("../tools/")
from time import time

# Import from custom utils
from utils.data_operations import remove_bad_records, add_features
from utils.data_operations import replace_NaNs, replace_Infs
from utils.poi_outliers import plot_outliers

#from sklearn.metrics import accuracy_score

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','salary'] # You will need to use more features

# Sourabh : Categorize All features into below categories
## 1. Direct Payments
## 2. Stock Options
## 3. Email Data

ALL_FEATURES = [
    'poi', 
    # Direct Payments
    'salary', 'deferral_payments', 'total_payments', 
    'bonus', 'deferred_income', 'long_term_incentive',
    'expenses', 'loan_advances', 'director_fees', 'other',
    # Stock Options
    'total_stock_value', 'exercised_stock_options', 
    'restricted_stock', 'restricted_stock_deferred', 
    # Email Data
    'from_messages', 'to_messages',
    'from_this_person_to_poi', 'from_poi_to_this_person', 
    'shared_receipt_with_poi'
    # Neutral Feature
    # 'email_address'
    ,'cost_to_company', 
    'stock_to_payment_ratio', 
    'email_pct_with_poi'
]

selected_features = [
    'poi',
    'salary', 'bonus', 'director_fees', 'other', 
    'total_payments',
    'total_stock_value', 'exercised_stock_options', 'restricted_stock',
    # More Features
    #'email_pct_with_poi', 'expenses', 'loan_advances'
]

final_features = [
    'poi',
    'salary', 'bonus', 'director_fees', 'other', 
    'total_payments',
    'total_stock_value', 'exercised_stock_options', 'restricted_stock',
    # More Features
    #'from_messages', 'expenses', 'loan_advances',
    # Added Features
    'cost_to_company', 
    'stock_to_payment_ratio', 
    'email_pct_with_poi'
]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
# Sourabh : Delete the "TOTAL" & "LOCKHART EUGENE E" as all fields are NaNs
data_dict = remove_bad_records(data_dict, 
                               ["TOTAL", "LOCKHART EUGENE E",
                                "THE TRAVEL AGENCY IN THE PARK"]
                                )

# Sourabh : Clean the data -- replace NaNs with ZERO
data_dict = replace_NaNs(data_dict)
data_dict = replace_Infs(data_dict)

# Sourabh : Plot the outliers using different features
plot_outliers(data_dict, "salary", "bonus")
plot_outliers(data_dict, "expenses", "other")
plot_outliers(data_dict, "total_payments", "total_stock_value")


### Task 3: Create new feature(s)
data_dict = add_features(data_dict)

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
#Sourabh -- comment the below line
data = featureFormat(my_dataset, selected_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
from sklearn.cross_validation import train_test_split
from utils.basic_models import naive_bayes_model, svm_model, decision_tree_model
from utils.basic_models import KNN_model

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.1, random_state=42)

# Sourabh: Build Basic Classifiers
#print '----- Basic Models ----'
#print "\nClassifer --- <Naive Bayes>"
#clf_NB = naive_bayes_model(features_train, labels_train, features_test, labels_test)
#test_classifier(clf_NB, my_dataset, selected_features)
#print '-'*30
#
#print "\nClassifer --- <SVM>"
#clf_SVM = svm_model(features_train, labels_train, features_test, labels_test)
#test_classifier(clf_SVM, my_dataset, selected_features)
#print '-'*30
#
#print "\nClassifer --- <Decision Tree>"
#clf_DT = decision_tree_model(features_train, labels_train, features_test, labels_test)
#test_classifier(clf_DT, my_dataset, selected_features)
#print '-'*30
#
#print "\nClassifer --- <KNN>"
#clf_KNN = KNN_model(features_train, labels_train, features_test, labels_test)
#test_classifier(clf_KNN, my_dataset, selected_features)
#print '-'*30

# Provided to give you a starting point. Try a variety of classifiers.

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

#from utils.advanced_models import rf_model, ET_model, ET_feature_importances
#from utils.advanced_models import bagging_classifer, ada_boost_classifer
#from sklearn.metrics import confusion_matrix
#
#
#print '----- Advanced Models ----'
#start = time()
#print "\nClassifer --- <Random Forest>"
#clf_rf = rf_model(features_train, labels_train, features_test, labels_test)
#test_classifier(clf_rf, my_dataset, selected_features)
#print '\nTime taken for the classifier : {} sec'.format(round(time() - start, 2))
#print '-'*30
#
#print "\nClassifer --- <Extra Trees Classifier>"
#start = time()
#clf_ET = ET_model(features_train, labels_train, features_test, labels_test)
#ET_feature_importances(clf_ET, selected_features)
#test_classifier(clf_ET, my_dataset, selected_features)
#print "\nConfusion Martix:\n"
#confusion_matrix(clf_ET.predict(features_test), labels_test)
#print '\nTime taken for the classifier : {} sec'.format(round(time() - start, 2))
#print '-'*30
#
#print "\nClassifer --- <Bagging Classifier>"
#start = time()
#clf_bagging = bagging_classifer(features_train, labels_train, features_test, labels_test)
#test_classifier(clf_bagging, my_dataset, selected_features)
#print '\nTime taken for the classifier : {} sec'.format(round(time() - start, 2))
#print '-'*30
#
#print "\nClassifer --- <Ada Boost Classifier>"
#start = time()
#clf_ada_boost = ada_boost_classifer(features_train, labels_train, features_test, labels_test)
#test_classifier(clf_ada_boost, my_dataset, selected_features)
#print '\nTime taken for the classifier : {} sec'.format(round(time() - start, 2))
#print '-'*30


## Sourabh: Pipeline SVC Model
from utils.pipeline_models import pipeline_SVC_model, pipeline_LSVC_model
from utils.pipeline_models import pipeline_KNN_model, pipeline_DT_model
from utils.pipeline_models import pipeline_RF_model, pipeline_LRegr_model

### SVC Pipeline Model
#print '----- SVC Pipeline Model ----'
#grid_search = pipeline_SVC_model(features_train, labels_train, features_test, labels_test)
#
#print "\nBest Estimator:"
#print "------------------"
#best_est = grid_search.best_estimator_
#print best_est
#print "SVC Best Model Score : ", best_est.score(features_test, labels_test)
#start = time()
#print "\nTest Classifer --- <Best KNN Pipeline Gridsearch Classifier>\n"
#test_classifier(best_est, my_dataset, selected_features)
#print '\nTime taken to test the classifier : {} sec'.format(round(time() - start, 2))
#print '-'*30


### LSVC Pipeline Model
#print '----- LSVC Pipeline Model ----'
#grid_search = pipeline_LSVC_model(features_train, labels_train, features_test, labels_test)
#
#print "\nBest Estimator:"
#print "------------------"
#best_est = grid_search.best_estimator_
#print best_est
#print "LSVC Best Model Score : ", best_est.score(features_test, labels_test)
#start = time()
#print "\nTest Classifer --- <Best KNN Pipeline Gridsearch Classifier>\n"
#test_classifier(best_est, my_dataset, selected_features)
#print '\nTime taken to test the classifier : {} sec'.format(round(time() - start, 2))
#print '-'*30
#
#### DT Pipeline Model
#print '----- DT Pipeline Model ----'
#grid_search = pipeline_DT_model(features_train, labels_train, features_test, labels_test)
#
#print "\nBest Estimator:"
#print "------------------"
#print best_est
#print "DT Best Model Score : ", best_est.score(features_test, labels_test)
#start = time()
#print "\nTest Classifer --- <Best KNN Pipeline Gridsearch Classifier>\n"
#test_classifier(best_est, my_dataset, selected_features)
#print '\nTime taken to test the classifier : {} sec'.format(round(time() - start, 2))
#print '-'*30

## KNN Pipeline Model
from sklearn.cross_validation import StratifiedShuffleSplit
cv = StratifiedShuffleSplit(labels, 100, test_size=0.1, random_state = 42)

print '----- KNN Pipeline Model ----'
#grid_search = pipeline_KNN_model(features_train, labels_train, features_test, labels_test, cv)
grid_search = pipeline_KNN_model(features, labels, cv)

print "\nBest Estimator:"
print "------------------"
#mask = grid_search.best_estimator_.named_steps['selection'].get_support()
#top_features = [x for (x, boolean) in zip(selected_features[1:], mask) if boolean]
n_pca_components = grid_search.best_estimator_.named_steps['reduce_dim'].n_components_

#print "\nTop Features : ", top_features
print "\nTop Components : ", n_pca_components

###################
# Print the parameters used in the model selected from grid search
print "\nBest Params: ", grid_search.best_params_ 
###################
    
clf = grid_search.best_estimator_
print "KNN Best Model Score : ", clf.score(features_test, labels_test)
start = time()
print "\nTest Classifer --- <Best KNN Pipeline Gridsearch Classifier>\n"
test_classifier(clf, my_dataset, selected_features)
print '\nTime taken to test the classifier : {} sec'.format(round(time() - start, 2))

#### RF Pipeline Model
#print '----- RF Pipeline Model ----'
#random_search = pipeline_RF_model(features_train, labels_train, features_test, labels_test)
#clf_rf_p = random_search.best_estimator_
#print "Random Search Best Model Score : ", clf_rf_p.score(features_test, labels_test)
#start = time()
#print "\nTest Classifer --- <RF Randomized Search Classifier>\n"
#test_classifier(clf_rf_p, my_dataset, selected_features)
#print '\nTime taken to test the classifier : {} sec'.format(round(time() - start, 2))

# Example starting point. Try investigating other evaluation techniques!
#start = time()
##print "\nTest Classifer --- <Best KNN Pipeline Gridsearch Classifier>\n"
#test_classifier(clf, my_dataset, selected_features)
#print '\nTime taken to test the classifier : {} sec'.format(round(time() - start, 2))

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

features_list = selected_features
dump_classifier_and_data(clf, my_dataset, features_list)