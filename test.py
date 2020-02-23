import requests
import time
from pymongo import MongoClient
import os

connectionString = "mongodb+srv://emily:<password>@cluster0-sutnn.mongodb.net/test"

client = MongoClient(connectionString)

#Find database "cryptocurrencyPrices"
db = client["cryptocurrencyPrices"]

#Find collection in database called "bitcoin"
mycol = db["bitcoin"]

#Current time
ts = time.time();
            
#Price of bitcoin
price = str(float(requests.get("https://api.coinbase.com/v2/prices/BTC-USD/buy")
                  .json()["data"]["amount"]))

myDict = { "timestamp": ts , "price": price}

#Add Dictionary key-value pairs as a document in MongoDB collection
x = mycol.insert_one(myDict)





    
    
