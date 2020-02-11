# any data relating to the four isotopes are stored in arrays as [U235, U238, Pu239, Pu241]

# fraction of the kth age group in the reactor core
# TODO make function to calculate this (12 element array) from bundle ages in DB
c_k = 0

# fission fractions for each of the 4 isotopes for each bundle age 
# TODO make this into a hash table (age : fission fraction array)?
f_i = 0

# released energy per fission of each of the four isotopes 
q_i = [202.36, 205.99, 211.12, 214.26]      #MeV
q_err = [0.26, 0.52, 0.34, 0.33]        #MeV

# Thermal power of the reactor for the selected period of time 
# TODO need net electrical power, elec power to run the plant and mech efficentcy of the 
# CANDU model, this is probably best done by preprocessing data to avoid redundancies 
p_th = 0        #MWh ? 

# Neutrino emission spectrum per fission per MeV 
# TODO find table of values for each of the four isotopes (x energy gives y emission)
# likley store this in the db
v_spectrum = 0      