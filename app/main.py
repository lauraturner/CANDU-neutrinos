import app.data_for_calc as data_for_calc
import app.bundle_age as bundle_age
from datetime import datetime, timedelta

# any data relating to the four isotopes are stored in arrays as [U235, U238, Pu239, Pu241]

# fraction of the kth age group in the reactor core
# TODO make function to calculate this (12 element array) from bundle ages in DB
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

def fuel_ratio(thermal_power, bundle_age, date):
    power_sum = 0
    day_pwr = thermal_power.loc[thermal_power['date'] == date]
    for age in bundle_age.keys():
        power_frac = 0
        for fuel in q_i.keys():
            age_fissions = f_i.loc[f_i['days'] == int(age)]
            power_frac += age_fissions[fuel].values[0] * q_i[fuel]
        power_sum += bundle_age[age] * power_frac
    return day_pwr['thermal_pwr'].values[0] / power_sum

def main(start, end, reactors):
    start = datetime.strptime(start, "%m/%d/%Y") # data period start
    end = datetime.strptime(end, "%m/%d/%Y") # data period end
    p_th = data_for_calc.get_thermal_data(start, end, reactors) # MWh 
    delta = end - start
    for i in range(delta.days + 1):
        date = start + timedelta(days=i)
        for reactor in reactors:
            bundle_ages = bundle_age.main(reactor, date, f_i)
            pwr_ratio = fuel_ratio(p_th[reactor], bundle_ages, date)




