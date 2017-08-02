#!/usr/bin/python
import numpy as np

def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []

    ### your code goes here
    errors = np.subtract(net_worths, predictions) ** 2
    
    p90 = np.percentile(errors, 90)
    print "90% Percentile : ", p90
    print "Removing errors more than 90%"

    for i in range(0, len(errors)):
        if errors[i] <= p90:
            cleaned_data.append((ages[i][0], net_worths[i][0], errors[i][0]))

    print cleaned_data
    return cleaned_data

