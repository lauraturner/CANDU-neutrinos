# CANDU-neutrinos
## Usage Notes

 - Spectrums calculated from the calculator are saved in the 'Data' folder in the project root directory in csv .txt files. File names consist of the reactor and the date range (inclusive)
 ex. A spectrum for BRUCE-G4 from 11/2/2019 to 12/3/2019 will have the file name `B-G4_11-2-1029_12-3-2019.txt` 
 
 - Warning: The calculator currently takes a long time to calculate spectrums (progress can be seen from the CLI when the calculator is running). 

## Installation
### Dependencies
Before installing make sure you have downloaded the following dependencies. 
 - Python 3 [https://www.python.org/downloads/]


### Installation

 1. From the CLI, navigate to the directory where you like to put the project.
 2. git clone the repo into the desired working directory.
 3. Navigate into the project root folder.
 4. Install python packages: `pip3 -r requirements.txt`
 5. Create a file in the root directory called .env.
 6. Copy the following into the .env file.
 `MONGO_URI=`
 
 7. Login to [https://www.mongodb.com/cloud/atlas
 8. (https://www.mongodb.com/cloud/atlas), navigate to the candu-data database and paste the URI string for the MongoDB database into the .env file and save it. (Go to https://docs.mongodb.com/guides/cloud/connectionstring for instructions on how to get the string). 
 NOTE: DO NOT SHARE THIS STRING OR COMMIT IT TO GITHUB, this string allows anyone access to the database.
 ex. `MONGO_URI="URIstring"`
 9. From the root folder run the `run.py` file using Python 3 to start the application. 
 10. Navigate to the local https address listed on the CLI once the application is running to visit the site.

 

## Database Structure:

This application uses MongoDB to host the database.

### Database name: 'reactors'

**Collection names:** 
 - 'BRUCEA-G1'
 - 'BRUCEA-G2' 
 - 'BRUCEA-G3' 
 - 'BRUCEA-G4' 
 - 'BRUCEB-G5'
 - 'BRUCEB-G6' 
 - 'BRUCEB-G7' 
 - 'BRUCEB-G8' 
 - 'DARLINGTON-G1' 
 - 'DARLINGTON-G2'
 - 'DARLINGTON-G3' 
 - 'DARLINGTON-G4' 
 - 'PICKERINGA-G1' 
 - 'PICKERINGA-G4'
 - 'PICKERINGB-G5' 
 - 'PICKERINGB-G6' 
 - 'PICKERINGB-G7' 
 - 'PICKERINGB-G8'

**Data Structure:** (for all collections in this DB)
 - date: [date time] 
 - thermal_pwr: [MWh/day]


### Database name: 'refueling'
Note: at this time the refueling data is mock data and each reactor has the same mock refueling data.

**Collection names:** 	

 - 'BRUCEA-G1'
 - 'BRUCEA-G2' 
 - 'BRUCEA-G3' 
 - 'BRUCEA-G4' 
 - 'BRUCEB-G5'
 - 'BRUCEB-G6' 
 - 'BRUCEB-G7' 
 - 'BRUCEB-G8' 
 - 'DARLINGTON-G1' 
 - 'DARLINGTON-G2'
 - 'DARLINGTON-G3' 
 - 'DARLINGTON-G4' 
 - 'PICKERINGA-G1' 
 - 'PICKERINGA-G4'
 - 'PICKERINGB-G5' 
 - 'PICKERINGB-G6' 
 - 'PICKERINGB-G7' 
 - 'PICKERINGB-G8'

**Data Structure:** (for all collections in this DB)
 - bundle_id: [channel number - bundle number]
		 - ex. channel 188, bundle 4. The bundle_id is: '188-4'
 - refuel_dates: [array of datetimes]


### Database name: 'fission_data'

**Collection name:** 'fission_fractions'
		**Data Structure:**
 - days: [days] 			
 - U235: [fraction of total fuel fissions] 			
 - U238: [fraction of total fuel fissions] 			
 - Pu239: [fraction of total fuel fissions] 			
 - Pu241: [fraction of total fuel fissions]

**Collection name:** 'fission_rates'
		**Data Structure:**
 - days: [days] 			
 - U235: [fissions/s]  			
 - U238: [fissions/s] 			
 - Pu239: [fissions/s] 			
 - Pu241: [fissions/s]

**Collection name:** 'nu_spectrum_candu'
		**Data Structure:**
 - energy_MeV: [MeV] 			
 - U235: [#nu per MeV per fission]  			
 - U238: [#nu per MeV per fission] 			
 - Pu239: [#nu per MeV per fission] 			
 - Pu241: [#nu per MeV per fission]
