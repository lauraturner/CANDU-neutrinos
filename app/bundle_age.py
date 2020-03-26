import app.database as db
import pandas as pd
import numpy as np
from datetime import datetime
import json


# Find how old each bundle in the reactor is
def get_bundle_age(date, bundles):
    ages = []
    for index, bundle in bundles.iterrows():
        days = []
        # calculate time between date and past refueling dates 
        for refuel_date in bundle['dates']:
            date_diff = (date - refuel_date).days
            if date_diff > 0:
                days.append(date_diff)
        # if bundle does not have a past refueling date, set to 100 days old 
        if len(days) == 0:
            ages.append(100)
        # choose the most recent refueling age
        elif len(days) == 1:
            ages.append(days[0])
        else:
            temp = np.min(days)
            ages.append(temp)
    return ages 

# format the data from the DB into a df
def data_to_dataframe(db_res, cols):
    data = []
    for doc in db_res:
        data.append(list(doc.values()))
    df = pd.DataFrame(np.array(data), columns=cols)
    return df

# find the element in an array that is closest to the given value
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# calculate the percent of bundles in each age group
def age_percent(age_count, bundles):
    age_sum = 0
    for age in age_count.keys():
        age_count[age] = age_count[age]/bundles
        age_sum += age_count[age]
    # if the percentages do not add to ~1.000 there is an issue here
    if age_sum < 0.999 or age_sum > 1.001:
        print('Please check bundle age calculator, age weight total: ' + str(age_sum))
    return age_count

# use bundle ages to find the percent in each age group from the DB
def age_weights(ages, fission_ages):
    age_count = {}
    # match the bundle age to the closest age group from the DB
    # and count the number of bundles in each group
    for age in ages:
        bundle_age = int(find_nearest(fission_ages, age))
        if bundle_age in age_count:
            age_count[bundle_age] += 1
        else:
            age_count[bundle_age] = 1
    return age_percent(age_count, len(ages))

# Calculate the weight of each fuel age present in the 
# reactor on a specific date
def main(reactor, date, fission_ages):
    cols = ['bundle_id', 'dates']
    res = db.find_in_db('refueling', reactor)
    data = data_to_dataframe(res, cols)
    ages = get_bundle_age(date, data)
    return age_weights(ages, fission_ages['days'])