import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')
myclient = pymongo.MongoClient(MONGO_URL)

def insert_into_db(collection, database, data):
    mydb = myclient[database]
    mycol = mydb[collection]
    res = mycol.insert_many(data)
    print(res)

def find_in_db(database, collection, query):
    mydb = myclient[database]
    mycol = mydb[collection]
    return mycol.find(query, {"_id": 0})


