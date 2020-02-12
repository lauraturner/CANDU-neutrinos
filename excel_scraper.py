import pandas as pd
from datetime import datetime
import json
from database import insert_into_db
import os

def format_reactor_data(reactor_info, reactor_data):
    reactor_objects = []
    for _, row in reactor_data.iterrows():
        thermal_pwr = (row['Net Energy'] + reactor_info['power_to_run'])/reactor_info['efficiency']
        date = datetime.strptime(row['Delivery Date'], "%m/%d/%Y")
        reactor_objects.append({'date': date, 'thermal_pwr': thermal_pwr})
    return reactor_objects

def parse_csv(path):
    drop_col = ['Measurement']
    hour_type = {}
    for i in range(1, 25): 
        hour = 'Hour ' + str(i)
        drop_col.append(hour)
        hour_type[hour] = 'float64'
    reactor_pwr = pd.read_csv(path, index_col=None, header=3)
    reactor_pwr = reactor_pwr.loc[reactor_pwr['Fuel Type'] == 'NUCLEAR']
    reactor_pwr = reactor_pwr.loc[reactor_pwr['Measurement'] == 'Output']
    reactor_pwr = reactor_pwr.astype(hour_type)
    reactor_pwr['Net Energy'] = reactor_pwr[hour_type.keys()].sum(axis=1, numeric_only=True)
    reactor_pwr = reactor_pwr.drop(drop_col, axis=1)
    return reactor_pwr

def insert_reactor_data(reactor_constants, reactor_pwr):
    for reactor in reactor_constants:
        reactor_data = reactor_pwr.loc[reactor_pwr['Generator'] == reactor['name']]
        reactor_objects = format_reactor_data(reactor, reactor_data)
        insert_into_db(reactor['name'], reactor_objects)

with open('reactor_constants.json', 'r') as f:
    reactor_constants = json.load(f)
folder = './reactor data/'
for filename in os.listdir(folder):
    csv_path = folder + filename
    reactor_pwr = parse_csv(csv_path)
    insert_reactor_data(reactor_constants, reactor_pwr)
    
    