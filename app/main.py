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
q_i = [202.36, 205.99, 211.12, 214.26]      #MeV
q_err = [0.26, 0.52, 0.34, 0.33]        #MeV 

# Neutrino emission spectrum per fission per MeV 
v_spectrum = data_for_calc.get_spectrum()      

def main(start, end, reactors):
    start = datetime.strptime(start, "%m/%d/%Y") # data period start
    end = datetime.strptime(end, "%m/%d/%Y") # data period end
    p_th = data_for_calc.get_thermal_data(start, end, reactors) # MWh 
    delta = end - start
    for i in range(delta.days + 1):
        date = start + timedelta(days=i)
        bundle_ages = bundle_age.main(reactors, date, f_i)





