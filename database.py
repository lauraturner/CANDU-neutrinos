import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')
myclient = pymongo.MongoClient(MONGO_URL)
mydb = myclient["reactors"]
reactors_names = ['BRUCEA-G1', 'BRUCEA-G2', 'BRUCEA-G3', 'BRUCEA-G4', 'BRUCEB-G5', 'BRUCEB-G6', 'BRUCEB-G7', 'BRUCEB-G8', 'DARLINGTON-G1', 'DARLINGTON-G2', 'DARLINGTON-G3', 'DARLINGTON-G4', 'PICKERINGA-G1', 'PICKERINGA-G4', 'PICKERINGB-G5', 'PICKERINGB-G6', 'PICKERINGB-G7', 'PICKERINGB-G8'  ]

def insert_into_db(collection, data):
    mycol = mydb[collection]
    res = mycol.insert_many(data)
    print(res)