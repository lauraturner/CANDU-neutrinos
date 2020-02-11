from pymongo import MongoClient
import os
# Get environment variables
MONGO_URL = os.getenv('MONGO_URL')

client = MongoClient(MONGO_URL)
db=client.CANDUdata