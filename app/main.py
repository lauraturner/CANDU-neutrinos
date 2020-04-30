import app.bundle_age as bundle_age
import app.database as db
import app.calculations as calc
import app.data_for_calc as data_for_calc
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os

# change df to json array to be sent to client
def format_json(spectrums, start, end):
    arr = []
    for reactor in spectrums.keys():
        spectrum = spectrums[reactor]
        arr.append({
            'reactor': reactor,
            'label': spectrum['energy_MeV'].tolist(),
            'data': spectrum['neutrinos'].tolist()
        })
    if (end - start).days == 0:
        arr[0]['dates']= start.strftime("%b %d, %Y")
    else:
        arr[0]['dates']= start.strftime("%b %d, %Y") + ' to ' + end.strftime("%b %d, %Y")
    return arr

# Save neutrino data as a .txt file with headers 
# in the ./Data folder, file name is the first letter of the 
# power plant, the genorator number then the start and end date
def save_data(reactor, spectrum, start, end):
    period = get_period(start, end)
    file_name = reactor[0] + '-' + reactor[-2:] + '_' + period + '.txt'
    cwd = os.getcwd()
    path = os.path.join(cwd, 'Data/').replace("\\", "/")
    if not os.path.exists(path):
        os.makedirs('Data')
    filepath = os.path.join(path, file_name)
    file_data = spectrum.to_csv(sep=',', index=False, header=True)
    with open(filepath, 'w') as f:
        f.write(file_data)

# get the time period of the data as a string
def get_period(start, end):
    delta_days = (end - start).days
    if delta_days == 0:
        return start.strftime("%m-%d-%Y")
    else:
        return start.strftime("%m-%d-%Y") + '_' + end.strftime("%m-%d-%Y") 

# number of days in the period
def get_num_days(start, end):
    delta = end - start
    return delta.days + 1

# get the daily neutrino spectrum 
def get_day_spectrum(reactor, p_th, date, f_i):
    bundle_ages = bundle_age.main(reactor, date, f_i) # percentage of bundles in each age group 
    return calc.calc_spectrum(p_th[reactor], bundle_ages, date, f_i)

# print calculator progress to CLI
def progress(days_done, num_days):
    print(str(days_done) + '/' + str(num_days) + ' Days finished')      

# Main function to control calculator
def main(start, end, reactors):
    start = datetime.strptime(start, "%m/%d/%Y") # data period start
    end = datetime.strptime(end, "%m/%d/%Y") # data period end
    num_days = get_num_days(start, end)
    # get Thermal data for the specified dates (inclusive)
    p_th = data_for_calc.get_thermal_data(start, end, reactors) # MeV/day
    # fission fractions for each of the 4 isotopes for each bundle age 
    f_i = data_for_calc.get_fission_fractions()
    spectrums = {}

    for reactor in reactors:
        spectrums[reactor] = calc.get_spec_df() #df to hold neutrino data

    # loop through each day in the given period
    for i in range(num_days):
        date = start + timedelta(days=i)
        # calculate neutrinos emmited from each reactor for the current date
        for reactor in reactors:
            day_spectrum = get_day_spectrum(reactor,p_th, date, f_i)
            # sum the neutrinos emitted for each day for each reactor
            spectrums[reactor]['neutrinos'] += day_spectrum['neutrinos']
        # print calculator progress
        progress(i + 1, num_days)

    for reactor in reactors:
        spectrums[reactor]['neutrinos'] = calc.average_neutrinos(num_days, spectrums[reactor])
        save_data(reactor, spectrums[reactor], start, end)
    return format_json(spectrums, start, end)
