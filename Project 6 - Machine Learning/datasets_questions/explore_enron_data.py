#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

print "Total number of data points(people) : ", len(enron_data)

print "Data for Mr. SKILLING JEFFREY K : \n ", enron_data["SKILLING JEFFREY K"]

print "No. of features for each person : ", len(enron_data["SKILLING JEFFREY K"])

print "Below are the persons with interest :"
poi_count = 0
for k, v in enron_data.items():
	if v["poi"] == True:
		print "\t", k
		poi_count += 1


print "Total number of POI(Person of Interest) : ", poi_count

### Load poi names from ../final_project/poi_names.txt
poi_names_file = "../final_project/poi_names.txt"
poi_names_count = 0
with open(poi_names_file, 'r') as f:
	for line in f:
		if line.startswith("(y)") or line.startswith("(n)"):
			poi_names_count += 1

print "Total number of POI(Person of Interest) from file : ", poi_names_count

print "Total value of stock belonging to James Prentice : ", enron_data["PRENTICE JAMES"]["total_stock_value"]
print "Number of email messages for Wesley Colwell : ", enron_data["COLWELL WESLEY"]['from_this_person_to_poi']
print "The value of stock options exercised by Jeffrey K Skilling : ", enron_data["SKILLING JEFFREY K"]["exercised_stock_options"]

max_total_payments = 0
max_total_payments_key = ""
for k, v in enron_data.items():
	total_payments = v["total_payments"]
	if total_payments == 'NaN' or k == "TOTAL":
		continue

	if total_payments >= max_total_payments :
		max_total_payments_key = k
		max_total_payments = v["total_payments"]


print "Max total payment was received by <{0}> with payment of <${1}>".format(max_total_payments_key, max_total_payments)


count_num_sal = 0
count_email = 0
count_nan_total_payments = 0
for k, v in enron_data.items():
	sal = str(v['salary'])
	email = v['email_address']
	total_payments = str(v['total_payments'])

	if sal.isdigit():
		count_num_sal += 1
	
	if email.endswith("@enron.com"):
		count_email += 1

	if total_payments == 'NaN':
		count_nan_total_payments += 1


print "Number of people who had valid salary & email IDs are respectively : ", count_num_sal, count_email
print "Percentage of people with NANs as total payment : ", count_nan_total_payments * 100 / len(enron_data)


poi_nan_total_payment_count = 0
for k, v in enron_data.items():
	if v["poi"] == True and v["total_payments"] == 'NaN':
		poi_nan_total_payment_count += 1

print "Percentage of POIs with NANs as total payment : ", poi_nan_total_payment_count * 100 / poi_count

count_nan_total_payments += 10
print "After adding 10 NAN POIs the NANs for total payments are -- ", (count_nan_total_payments * 100) / (len(enron_data) + 10)

poi_count += 10
print "After adding 10 NAN -- number of POIs : ", poi_count
print "After adding 10 NAN -- Percentage of POIs with NANs as total payment : ", (poi_nan_total_payment_count  + 10) * 100 / poi_count

