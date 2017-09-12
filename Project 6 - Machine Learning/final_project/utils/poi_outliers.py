#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: sourabh
Outliers Detection
"""
import sys
sys.path.append("../../tools/")
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from feature_format import featureFormat
import numpy as np


def plot_outliers(data_dict, feature_1, feature_2):
    '''
    This function takes 2 features at a time and 
    finds outlier, here more than 95th Percentile
    is being considered as an outlier
    :param data_dict: Data Dictionary of all features for the POIs
    :param feature_1: 1st Feature plotted against x-axis
    :param feature_2: 2nd Feature plotted against y-axis
    :return: New Dataset with NaNs replaced with ZERO
    '''
    ### read in data dictionary, convert to numpy array
    features = [ feature_1, feature_2 ]
    data = featureFormat(data_dict, features)
    
    feature_1_outlier = np.percentile(data[:, 0], 95)
    feature_2_outlier = np.percentile(data[:, 1], 95)

    print "-- Total {} & {} Values Outliers --".format(feature_1, feature_2)
    for k, v in data_dict.items():
        if v[feature_1] >= feature_1_outlier:
            if v[feature_2] >= feature_2_outlier/2:
                print "{} --- {} <{}>, {} <{}>, POI <{}>"\
                    .format(k, feature_1, v[feature_1], 
                            feature_2, v[feature_2], v["poi"])
        elif v[feature_2] >= feature_2_outlier:
            if v[feature_1] >= feature_1_outlier/2:
                print "{} --- {} <{}>, {} <{}>, POI <{}>"\
                    .format(k, feature_1, v[feature_1], 
                            feature_2, v[feature_2], v["poi"])


    for row in data:
        feature_1_i = row[0]
        feature_2_i = row[1]
        if feature_1_i >= feature_1_outlier and feature_2_i >= feature_2_outlier/2:
            plt.scatter( feature_1_i, feature_2_i, 
                                      color = 'r', marker = '*')
        elif feature_2_i >= feature_2_outlier and feature_1_i >= feature_1_outlier/2:
            plt.scatter( feature_1_i, feature_2_i, 
                                      color = 'r', marker = '*')
        else:
            plt.scatter( feature_1_i, feature_2_i, 
                                      color = 'g', marker = '+')
    
    plt.xlabel( feature_1 )
    plt.ylabel( feature_2 )
    plt.title( "Outlier Detection \n{} vs {}".format(feature_1, feature_2) )
    
    plt.show()
