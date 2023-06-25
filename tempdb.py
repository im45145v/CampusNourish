import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb+srv://21311a6611:[pass]@cluster0.ub5pbd6.mongodb.net/?retryWrites=true&w=majority',serverSelectionTimeoutMS=60000)
db = client["Food"]
collection = db["Recipes"]
maggie = {'dish_name':'maggie','ingredients':['water,maggie,salt'],'calories':34,'protein':12,'carbohydrates':29,'fat':2,'fiber':6}
collection.insert_one(maggie)
client.close()