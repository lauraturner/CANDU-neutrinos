from database import find_in_db
import pandas as pd
import numpy as np

# names of the fuels used
FUELS = ['U235', 'U238', 'Pu239', 'Pu241']

# format db cursor into a dataframe with specified columss 
def data_to_dataframe(db_res, cols):
    data = []
    for doc in db_res:
        data.append(list(doc.values()))
    df = pd.DataFrame(np.array(data), columns=cols)
    return df

# pull the CANDU nuetrino spectrum from the db and format into a df
def get_spectrum():
    cols = ['energy_MeV'] + FUELS
    res = find_in_db('fission_data', 'nu_spectrum_candu')
    nu_spectrum = data_to_dataframe(res, cols)
    return nu_spectrum

# pull the fission fractions per bundle age from the db and format into a df
def get_fission_fractions():
    cols = ['days'] + FUELS
    res = find_in_db('fission_data', 'fission_fractions')
    fission_fractions = data_to_dataframe(res, cols)
    return fission_fractions

# pull the thermal power for the specified reactors and time period
# from the db, returns an array of the reactors and their data in a df
def get_thermal_data(start, end, reactors):
    database = "reactors"
    query = {"date": {"$gte": start, "$lte": end}}
    thermal_pwr = []
    for reactor in reactors:
        power_obj = {'reactor': reactor}
        res = find_in_db(database, reactor, query)
        power_obj['data'] = data_to_dataframe(res, ['date', 'thermal_pwr'])
        thermal_pwr.append(power_obj)
    return thermal_pwr

