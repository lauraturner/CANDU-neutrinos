import pymongo
import os
from dotenv import load_dotenv

# load mongodb URI from .env and connect
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
MYCLIENT = pymongo.MongoClient(MONGO_URI)

# insert data into a specific db and collection
def insert_into_db(database, collection, data):
    mydb = MYCLIENT[database]
    mycol = mydb[collection]
    res = mycol.insert_many(data)


# find data from a specific db and collection using a 
# query if needed. _ids are never used in this program 
# so they are omitted 
def find_in_db(database, collection, query = {}):
    mydb = MYCLIENT[database]
    mycol = mydb[collection]
    return mycol.find(query, {"_id": 0})


