#!//anaconda/bin/python
# Code to Reformat the titanic CSV data into more meaningful units

import pandas as pd
import numpy as np
import scipy as sp
import sys

#### Function to split name into Salutation, First Name, Middle Name, Last Name
def split_name(name):
    last_name, fm_name = tuple(name.split('(')[0].split(','))
    fm_name = fm_name.split()
    salutation, first_name, middle_name = '', '', ''
    try:
        salutation = fm_name[0]
        first_name = fm_name[1]
        middle_name = fm_name[2]
    except IndexError:
        pass
    return salutation.strip(), first_name.strip(), middle_name.strip(), last_name.strip()


def reformat():
	# Read the CSV file
	titanic_df = pd.read_csv('../data/data_original.csv')
	
	# New Data Frame to write csv data as output
	df = pd.DataFrame();

	# Get no of rows and columns
	num_rows, num_columns = titanic_df.shape


	df['PassengerID'] = titanic_df['PassengerId']
	df['Age'] = titanic_df['Age']
	df['Fare'] = titanic_df['Fare'].round(2)

	### Clean & arrange the data points

	# Split Name into Parts
	df['Salutation'], df['First_Name'], df['Middle_Name'], df['Last_Name'] = titanic_df['Name'].apply(split_name).str

	# Create Survival Label Column -- will be helpful for ploting
	df['Survival'] = titanic_df.Survived.map({0 : 'Died', 1 : 'Survived'})
	
	# Change Male/Female to M/F
	df['Sex'] = titanic_df['Sex'].replace(to_replace=['male', 'female'], value=['Male', 'Female'])

	# Create Pclass Label Column -- will be helpful for ploting
	df['Class'] = titanic_df.Pclass.map({1 : 'First Class', 2 : 'Second Class', 3 : 'Third Class'})
	df['Embarked'] = titanic_df.Embarked.map({'C' : 'Cherbourg', 'Q' : 'Queenstown', 'S' : 'Southampton'})

	# Create a new attribute for counting Family members
	df['Family_Members_Count'] = titanic_df['SibSp'] + titanic_df['Parch']

	# Create age groups & assign age groups to passengers
	df['Age_Group'] = pd.cut(titanic_df['Age'], 
       bins=[0, 15, 25, 40, 55, 70, 90],
       labels=['Child', 'Youth', 'Adult', 'Mid-Age', 'Old', 'Very Old']
      )

	# Write data frame to CSV file data.csv
	df.to_csv('../data/data_titanic.csv', encoding='utf-8', index=False);


if __name__ == "__main__":
	print 'Python version :: ', sys.version
	print 'Pandas version :: ', pd.__version__
	print 'Numpy version :: ', np.__version__
	print 'Scipy version :: ', sp.__version__

	reformat();

