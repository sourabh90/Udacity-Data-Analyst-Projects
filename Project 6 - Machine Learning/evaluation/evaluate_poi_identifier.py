#!/usr/bin/python


"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
import numpy as np
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



### your code goes here 
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score

features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size = 0.3, random_state = 42)

print "Persons in Test Set : ", np.size(features_test)

clf = DecisionTreeClassifier()
clf.fit(features_train, labels_train)
print "Accuracy : ", clf.score(features_test, labels_test)

pred = clf.predict(features_test)
print "POIs predicted : ", np.sum(pred)

# If everybody predicted as non-poi, i.e., 0
print "If everyone is predicted as Non-POI, then accuracy would be :: ", (np.size(features_test) - np.sum(pred)) / np.size(features_test)

# Did you get any True Positives -- Prediction is POI and the person is an actual POI
count_poi = 0 
for i in range(len(labels_test)):
	if pred[i] == labels_test[i] and pred[i] == 1.0 :
		count_poi += 1

print "Total True Positives(Both Actual & Predicted POI) count :: ", count_poi

# Confusion Matrix
print " ------ Confusion Matrix ------"
print confusion_matrix(features_test, pred)
print "Precision Score :: ", precision_score(features_test, pred, average = "macro")
print "Recall Score :: ", recall_score(features_test, pred, average = "macro")



