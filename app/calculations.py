import pandas as pd
import numpy as np
import app.database as db
from operator import add
import app.data_for_calc as data_for_calc

# any data relating to the four isotopes are stored in arrays as [U235, U238, Pu239, Pu241]

# fraction of the kth age group in the reactor core
c_k = 0

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

# format a df for spectrum data
def get_spec_df():
    energy = v_spectrum['energy_MeV'].tolist()
    d = {'energy_MeV': energy, 'neutrinos': np.zeros(len(energy))}
    spectrum = pd.DataFrame(data=d)
    spectrum.set_index('energy_MeV')
    return spectrum

# calc the average number of nuetrinos per second for the period
def average_neutrinos(num_days, reactor_spec):
    seconds = (num_days)*24*60*60
    return reactor_spec['neutrinos']/seconds

# Calculate the number of fissions per MeV for a given bundle age group
def power_calc(age, bundle_age, f_i):
    power_frac = 0
    # sum the products of the fission fractions and energy released per fission
    # for each fuel type
    for fuel in q_i.keys():
        age_fissions = f_i.loc[f_i['days'] == int(age)]
        power_frac += age_fissions[fuel].values[0] * q_i[fuel]
    # Multiply the sum by the precent of bundles in that age group
    return bundle_age[age] * power_frac

# Calculate the spectrum for each energy level for a given bundle age group
def spectrum_age_sum(age, bundle_age, f_i):
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

def calc_spectrum(thermal_power, bundle_age, date, f_i):
    power_sum = 0
    spec_sum = np.zeros(len(v_spectrum['energy_MeV'].tolist()))
    day_pwr = thermal_power.loc[thermal_power['date'] == date] 
    day_spectrum = get_spec_df()
    for age in bundle_age.keys():
        # Calculate the spectrum with fission fractions for the age group
        spectrum = spectrum_age_sum(age, bundle_age, f_i)
        # Sum the calculated spectrum for each MeV level
        spec_sum = list(map(add, spectrum, spec_sum))
        # Sum the MeV per fission for each age group 
        power_sum += power_calc(age, bundle_age, f_i)
    # calculate the number of fissions for the date and then multiply this 
    # by each spectrum energy level to get neutrinos emitted per MeV for the day
    fissions = day_pwr['thermal_pwr'].values[0] / power_sum
    spec_sum = [x * fissions for x in spec_sum]
    # format a df to hold results
    day_spectrum['neutrinos'] = spec_sum
    return day_spectrum