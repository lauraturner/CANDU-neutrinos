import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')
myclient = pymongo.MongoClient(MONGO_URL)
mydb = myclient["reactors"]

def insert_into_db(collection, data):
    mycol = mydb[collection]
    res = mycol.insert_many(data)
    print(res)
