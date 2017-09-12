#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
@author: sourabh
DATA Operations
"""
import pandas as pd

def remove_bad_records(data_dict, keys_to_remove):
    '''
    This function takes a list of person names(dict keys) as 
    outliers/bad records; and remove them from the dictionary
    :param data_dict: Data Dictionary of all features for the POIs
    :param keys_to_remove : Keys/POIs to remove from the dataset
    :return: Removed mentioned keys and return new data set
    '''
    for key in keys_to_remove:
        del data_dict[key]

    return data_dict


def replace_NaNs(data_dict):
    '''
    This function replaces all the NaN values with ZERO
    from the entire dataset dictionary
    :param data_dict: Data Dictionary of all features for the POIs
    :return: New Dataset with NaNs replaced with ZERO
    '''
    for poi, poi_record in data_dict.items():
        for feature, feature_value in poi_record.items():
            if feature_value == 'NaN':
                data_dict[poi][feature] = 0

    return data_dict 


def replace_Infs(data_dict):
    '''
    This function replaces all the NaN values with ZERO
    from the entire dataset dictionary
    :param data_dict: Data Dictionary of all features for the POIs
    :return: New Dataset with NaNs replaced with ZERO
    '''
    for poi, poi_record in data_dict.items():
        for feature, feature_value in poi_record.items():
            if isinstance(feature_value, str) and feature_value.lower() == 'inf':
                data_dict[poi][feature] = 0

    return data_dict 
    
    
def add_features(data_dict):
    '''
    This function will create few new features using the 
    available features, and return new dataset.
    :param data_dict: Dataset in dictionary format
    :return: New Dataset with new features included
    '''
    # Convert to pandas dataframe for easier operations
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    
    # Total Payment + Total Stock Value
    df['cost_to_company'] = df['total_payments'] + df['total_stock_value']
    
    # Stock to Payment ratio
    df['stock_to_payment_ratio'] = df['total_stock_value'] / (df['total_payments'] + 1)
    df['stock_to_payment_ratio'] = df['stock_to_payment_ratio'].round(2)    

    # Percent of emails with POI
    df['email_pct_with_poi'] =  (df['from_this_person_to_poi'] + 
             df['from_poi_to_this_person'] + 
             df['shared_receipt_with_poi']) / (df['from_messages'] + df['to_messages'] + 1)
    df['email_pct_with_poi'] = df['email_pct_with_poi'].round(2)
    
    # Convert the dataframe back to dictionary
    data_dict = pd.DataFrame.to_dict(df, orient='index')
    
    return data_dict                      