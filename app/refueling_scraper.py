import pandas as pd
import json
import database as db
import os
import numpy as np

# parse the power csv for what data needs to go into the db.
def parse_csv(path):
    refueling_data = pd.read_excel(path, index_col=None)
    return refueling_data

# for each reactor: format the data and insert in the db
def insert_reactor_data(reactors, refueling_data):
    for reactor in reactors:
        db.insert_into_db(reactor['name'], 'refueling',  refueling_data)

# format excel data into objects for the DB
def format_bundles(refueling_data):
    temp_refueling = {}
    db_refueling=[]
    for _ , row in refueling_data.iterrows():
        bundles  = row['bundles'].split(',')
        for bundle in bundles:
            name = str(row['channel']) + '-' + bundle
            if name in temp_refueling:
                temp_refueling[name].append(row['date'])
            else:
                temp_refueling[name] = [row['date']]
    for key in temp_refueling:
        fuel_dict = {
            'bundle_id': key,
            'refuel_dates': temp_refueling[key]
        }
        db_refueling.append(fuel_dict)
    return db_refueling

def load_reactor_constants():
    with open('reactor_constants.json', 'r') as f:
        return json.load(f)

# main func to load reactor daily power data,
# parse the contents to get the daily net power [MWh]
# per reactor, then add it to the db  
def main():
    csv_path = './reactor data/mock_refueling_data.xlsx'
    reactors = load_reactor_constants()
    refueling_data = parse_csv(csv_path)
    refueling_data = format_bundles(refueling_data)
    insert_reactor_data(reactors, refueling_data)

if __name__== "__main__":
    main()

    
    