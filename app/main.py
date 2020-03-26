import app.data_for_calc as data_for_calc
import app.bundle_age as bundle_age
from app.plot import plot_neutrinos
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from operator import add


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

def power_calc(age):
    power_frac = 0
    for fuel in q_i.keys():
        age_fissions = f_i.loc[f_i['days'] == int(age)]
        power_frac += age_fissions[fuel].values[0] * q_i[fuel]
    return power_frac

def spectrum_calc(age, bundle_age):
    spec_sum = []
    for index, row in v_spectrum.iterrows():
        spec_frac = 0
        for fuel in q_i.keys():
            age_fissions = f_i.loc[f_i['days'] == int(age)]
            spec_frac += age_fissions[fuel].values[0] * row[fuel]
        spec_sum.append(bundle_age[age] * spec_frac)
    return spec_sum

def calc(thermal_power, bundle_age, date):
    power_sum = 0
    spec_sum = np.zeros(len(v_spectrum['energy_MeV'].tolist()))
    day_pwr = thermal_power.loc[thermal_power['date'] == date]
    day_spectrum = get_spec_df()
    for age in bundle_age.keys():
        spectrum = spectrum_calc(age, bundle_age)
        spec_sum = list(map(add, spectrum, spec_sum))
        power_frac = power_calc(age)
        power_sum += bundle_age[age] * power_frac
    power_ratio = day_pwr['thermal_pwr'].values[0] / power_sum
    spec_sum = [x * power_ratio for x in spec_sum]
    day_spectrum['add_spec'] = spec_sum
    day_spectrum['neutrinos'] += day_spectrum['add_spec']
    del day_spectrum['add_spec']
    return day_spectrum

def get_spec_df():
    energy = v_spectrum['energy_MeV'].tolist()
    d = {'energy_MeV': energy, 'neutrinos': np.zeros(len(energy))}
    spectrum = pd.DataFrame(data=d)
    spectrum.set_index('energy_MeV')
    return spectrum

def main(start, end, reactors):
    start = datetime.strptime(start, "%m/%d/%Y") # data period start
    end = datetime.strptime(end, "%m/%d/%Y") # data period end
    p_th = data_for_calc.get_thermal_data(start, end, reactors) # MWh 
    delta = end - start
    spectrums = {}
    for reactor in reactors:
        spectrums[reactor] = get_spec_df()
    for i in range(delta.days + 1):
        date = start + timedelta(days=i)
        print(date)
        for reactor in reactors:
            bundle_ages = bundle_age.main(reactor, date, f_i)
            day_spectrum = calc(p_th[reactor], bundle_ages, date)
            spectrums[reactor]['neutrinos'] += day_spectrum['neutrinos']
    for reactor in reactors:
        seconds = (delta.days + 1)*24*60*60
        spectrums[reactor]['neutrinos'] = spectrums[reactor]['neutrinos']/seconds 
    plot_neutrinos(spectrums, start, end)