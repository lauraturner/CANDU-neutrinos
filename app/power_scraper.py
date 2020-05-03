import pandas as pd
from datetime import datetime
import json
from database import insert_into_db
import os

# format csv data into objects to be inserted into the db. daily thermal 
# power is calculated from the net daily power, power to run and reactor 
# efficiency
def format_reactor_data(reactor_info, reactor_data):
    reactor_objects = []
    for _, row in reactor_data.iterrows():
        thermal_pwr = (row['Net Energy'] + reactor_info['power_to_run'])/reactor_info['efficiency']
        date = datetime.strptime(row['Delivery Date'], "%m/%d/%Y")
        reactor_objects.append({'date': date, 'thermal_pwr': thermal_pwr})
    return reactor_objects

# make the column labels needed for formating: hourly power
# data needs to be type float64 to sum for daily power. 
# after this measurment and hourly data colunms need to be deleted
def get_cols_to_format():
    drop_cols = ['Measurement']
    hour_types = {}
    for i in range(1, 25): 
        hour = 'Hour ' + str(i)
        drop_cols.append(hour)
        hour_types[hour] = 'float64'
    return drop_cols, hour_types

# parse the power csv for what data needs to go into the db.
# only keeps nuclear data its power output. power data is hourly, 
# so the rows are summed to get the daily net power output [MWh]
# the rest of the data is deleted
def parse_csv(path):
    reactor_pwr = pd.read_csv(path, index_col=None, header=3)
    reactor_pwr = reactor_pwr.loc[reactor_pwr['Fuel Type'] == 'NUCLEAR']
    reactor_pwr = reactor_pwr.loc[reactor_pwr['Measurement'] == 'Output']
    drop_cols, hour_types = get_cols_to_format()
    reactor_pwr = reactor_pwr.astype(hour_types)
    reactor_pwr['Net Energy'] = reactor_pwr[hour_types.keys()].sum(axis=1, numeric_only=True)
    reactor_pwr = reactor_pwr.drop(drop_cols, axis=1)
    return reactor_pwr

# for each reactor: format the data and insert in the db
def insert_reactor_data(reactor_constants, reactor_pwr):
    for reactor in reactor_constants:
        reactor_data = reactor_pwr.loc[reactor_pwr['Generator'] == reactor['name']]
        reactor_objects = format_reactor_data(reactor, reactor_data)
        insert_into_db('reactors', reactor['name'],  reactor_objects)

# load the JSON that stores each reactors' efficiency 
# and daily power needed to operate [MWh] (average)
def load_power_constants():
    with open('reactor_constants.json', 'r') as f:
        return json.load(f)

# main func to load reactor daily power data,
# parse the contents to get the daily net power [MWh]
# per reactor, then add it to the db  
def main():
    reactor_pwr_consts = load_power_constants()
    folder = './reactor data/thermal power/'
    for filename in os.listdir(folder):
        csv_path = folder + filename
        reactor_pwr = parse_csv(csv_path)
        insert_reactor_data(reactor_pwr_consts, reactor_pwr)

if __name__== "__main__":
    main()

    
    