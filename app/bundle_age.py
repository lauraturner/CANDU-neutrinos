import database as db
import pandas as pd
import numpy as np
from datetime import datetime
import json

def get_bundle_age(date, bundles):
    ages = []
    for index, bundle in bundles.iterrows():
        days = []
        for refuel_date in bundle['dates']:
            date_diff = (date - refuel_date).days
            if date_diff > 0:
                days.append(date_diff)
        if len(days) == 0:
            ages.append(100)
        else:
            ages.append(np.min(days))
    return ages 

def data_to_dataframe(db_res, cols):
    data = []
    for doc in db_res:
        data.append(list(doc.values()))
    df = pd.DataFrame(np.array(data), columns=cols)
    return df

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def age_percent(age_count, bundles):
    for age in age_count.keys():
        age_count[age] = age_count[age]/bundles
    return age_count

def age_weights(ages, fission_ages):
    age_count = {}
    for age in ages:
        bundle_age = int(find_nearest(fission_ages, age))
        if bundle_age in age_count:
            age_count[bundle_age] += 1
        else:
            age_count[bundle_age] = 1
    return age_percent(age_count, len(ages))

def main(reactors, date, fission_ages):
    bundle_ages = {}
    for reactor in reactors:
        cols = ['bundle_id', 'dates']
        res = db.find_in_db('refueling', reactor)
        data = data_to_dataframe(res, cols)
        ages = get_bundle_age(date, data)
        bundle_ages[reactor] = age_weights(ages, fission_ages['days'])
    return bundle_ages