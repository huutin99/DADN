from flask import Flask
from flask_pymongo import pymongo
#from app import app
CONNECTION_STRING = "mongodb+srv://dadn:dadn@dadn-xpn71.azure.mongodb.net/DADN?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('DADN')
user_collection = pymongo.collection.Collection(db, 'user_collection')