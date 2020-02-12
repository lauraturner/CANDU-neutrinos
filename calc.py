import data_for_calc 
from datetime import datetime

# any data relating to the four isotopes are stored in arrays as [U235, U238, Pu239, Pu241]

# fraction of the kth age group in the reactor core
# TODO make function to calculate this (12 element array) from bundle ages in DB
c_k = 0

# fission fractions for each of the 4 isotopes for each bundle age 
f_i = data_for_calc.get_fission_fractions()

# released energy per fission of each of the four isotopes 
q_i = [202.36, 205.99, 211.12, 214.26]      #MeV
q_err = [0.26, 0.52, 0.34, 0.33]        #MeV

# Thermal power of the reactor for the selected period of time  
start = datetime.strptime("6/1/2019", "%m/%d/%Y") # data period start
end = datetime.strptime("6/10/2019", "%m/%d/%Y") # data period end
reactors = ['BRUCEA-G1', 'BRUCEA-G2', 'DARLINGTON-G3', 'PICKERINGB-G8'] # reactors to retrive data from
p_th = data_for_calc.get_thermal_data(start, end, reactors)   #MWh  

# Neutrino emission spectrum per fission per MeV 
v_spectrum = data_for_calc.get_spectrum()      