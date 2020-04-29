import app.data_for_calc as data_for_calc
import app.bundle_age as bundle_age
import app.database as db
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from operator import add
import os

# any data relating to the four isotopes are stored in arrays as [U235, U238, Pu239, Pu241]

# fraction of the kth age group in the reactor core
c_k = 0

# fission fractions for each of the 4 isotopes for each bundle age 
f_i = data_for_calc.get_fission_fractions()

# released energy per fission of each of the four isotopes 
q_i = {
    'U235': 202.36, 
    'U238': 205.99,
    'Pu239': 211.12, 
    'Pu241': 214.26
   }   #MeV

q_err = [0.26, 0.52, 0.34, 0.33]        #MeV 

# Neutrino emission spectrum per fission per MeV 
v_spectrum = data_for_calc.get_spectrum() 

def retrive_data():
    data = []
    res = db.find_in_db('temp_data', 'results')
    for doc in res:
        data.append(doc)
    return data

# Calculate the number of fissions per MeV for a given bundle age group
def power_calc(age, bundle_age):
    power_frac = 0
    # sum the products of the fission fractions and energy released per fission
    # for each fuel type
    for fuel in q_i.keys():
        age_fissions = f_i.loc[f_i['days'] == int(age)]
        power_frac += age_fissions[fuel].values[0] * q_i[fuel]
    # Multiply the sum by the precent of bundles in that age group
    return bundle_age[age] * power_frac

# Calculate the spectrum for each energy level for a given bundle age group
def spectrum_age_sum(age, bundle_age):
    spec_sum = []
    for _, row in v_spectrum.iterrows():
        spec_frac = 0
        # sum the products of the fission fractions with the spectrum for each fuel type
        for fuel in q_i.keys():
            age_fissions = f_i.loc[f_i['days'] == int(age)]
            spec_frac += age_fissions[fuel].values[0] * row[fuel]
        # Multiply the sum by the precent of bundles in that age group
        spec_sum.append(bundle_age[age] * spec_frac)
    return spec_sum

def calc_spectrum(thermal_power, bundle_age, date):
    power_sum = 0
    spec_sum = np.zeros(len(v_spectrum['energy_MeV'].tolist()))
    day_pwr = thermal_power.loc[thermal_power['date'] == date] 
    day_spectrum = get_spec_df()
    for age in bundle_age.keys():
        # Calculate the spectrum with fission fractions for the age group
        spectrum = spectrum_age_sum(age, bundle_age)
        # Sum the calculated spectrum for each MeV level
        spec_sum = list(map(add, spectrum, spec_sum))
        # Sum the MeV per fission for each age group 
        power_sum += power_calc(age, bundle_age)
    # calculate the number of fissions for the date and then multiply this 
    # by each spectrum energy level to get neutrinos emitted per MeV for the day
    fissions = day_pwr['thermal_pwr'].values[0] / power_sum
    spec_sum = [x * fissions for x in spec_sum]
    # format a df to hold results
    day_spectrum['neutrinos'] = spec_sum
    return day_spectrum

# format a df for spectrum data
def get_spec_df():
    energy = v_spectrum['energy_MeV'].tolist()
    d = {'energy_MeV': energy, 'neutrinos': np.zeros(len(energy))}
    spectrum = pd.DataFrame(data=d)
    spectrum.set_index('energy_MeV')
    return spectrum

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
    arr[0]['dates']= start.strftime("%b %d, %Y") + ' to ' + end.strftime("%b %d, %Y")
    return arr

def save_data(reactor, spectrum, period):
    file_name = reactor[0] + '-' + reactor[-2:] + '_' + period + '.txt'
    cwd = os.getcwd()
    path = os.path.join(cwd, 'Data/').replace("\\", "/")
    if not os.path.exists(path):
        os.makedirs('Data')
    filepath = os.path.join(path, file_name)
    file_data = spectrum.to_csv(sep=',', index=False, header=True)
    with open(filepath, 'w') as f:
        f.write(file_data)

def main(start, end, reactors):
    start = datetime.strptime(start, "%m/%d/%Y") # data period start
    end = datetime.strptime(end, "%m/%d/%Y") # data period end
    p_th = data_for_calc.get_thermal_data(start, end, reactors) # MeV/day
    delta = end - start
    spectrums = {}
    num_days = delta.days + 1
    for reactor in reactors:
        spectrums[reactor] = get_spec_df() #df to hold neutrino data
    # loop through each day in the given period
    for i in range(num_days):
        date = start + timedelta(days=i)
        # calculate neutrinos emmited from each reactor for the current date
        for reactor in reactors:
            bundle_ages = bundle_age.main(reactor, date, f_i) # percentage of bundles in each age group 
            day_spectrum = calc_spectrum(p_th[reactor], bundle_ages, date)
            # sum the neutrinos emitted for each day for each reactor
            spectrums[reactor]['neutrinos'] += day_spectrum['neutrinos']
        # print calculator progress
        days_done = i + 1
        print(str(days_done) + '/' + str(num_days) + ' Days finished')
    for reactor in reactors:
        # calculate neutrinos emitted per second for the time period
        seconds = (delta.days + 1)*24*60*60
        spectrums[reactor]['neutrinos'] = spectrums[reactor]['neutrinos']/seconds
        period = start.strftime("%m-%d-%Y") + '_' + end.strftime("%m-%d-%Y") 
        save_data(reactor, spectrums[reactor], period)
    return format_json(spectrums, start, end)
