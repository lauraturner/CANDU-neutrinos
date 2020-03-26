import pymongo
import os
from dotenv import load_dotenv

# load mongodb URI from .env and connect
load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')
MYCLIENT = pymongo.MongoClient(MONGO_URL)

# insert data into a specific db and collection
def insert_into_db(collection, database, data):
    mydb = MYCLIENT[database]
    mycol = mydb[collection]
    res = mycol.insert_many(data)
    print(res)

# find data from a specific db and collection using a 
# query if needed. _ids are never used in this program 
# so they are omitted 
def find_in_db(database, collection, query = {}):
    mydb = MYCLIENT[database]
    mycol = mydb[collection]
    return mycol.find(query, {"_id": 0})

