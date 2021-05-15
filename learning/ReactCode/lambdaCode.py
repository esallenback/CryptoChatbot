import datetime
import requests
import time    
from pymongo import MongoClient

def lambda_handler(event, context):
    list = ['BTC', 'ETH',
            'LTC', 'DAI',
            'EOS', 'XLM',
            'BAT', 'XRP',
            'LINK', 'DASH',
            'XTZ', 'ZEC', 'REP']
    length = len(list)

    client = MongoClient("mongodb+srv://emilys:UIUCchatbot@cluster0-ar3em.mongodb.net/test?retryWrites=true&w=majority")
    db = client["cryptocurrencyChatbot"]

    # Iterating the index 
    # same as 'for i in range(len(list))' 
    for i in range(length):
        mycol = db[list[i]]
        #time.sleep(10)
        
        #Price of crypto
        timestamp = datetime.datetime.fromtimestamp(1575297000).isoformat()
        price = str(float(requests.get("https://api.coinbase.com/v2/prices/" + list[i] + "-USD/buy").json()["data"]["amount"]))
        

        
        url = "https://api.cryptowat.ch/markets/kraken/" + list[i] + "usd/summary"
        response = requests.request("GET", url)
        
        #Absolute change in crypto
        change = str(response.json()["result"]["price"]["change"]["absolute"])

        #Percent change in crypto
        #print("Percent change for " + list[i] + "(24hrs): " +
        #          str(response.json()["result"]["price"]["change"]["percent"]))
        
        #High for crypto
        high = str(response.json()["result"]["price"]["high"])
        
        #Low for crypto
        low = str(response.json()["result"]["price"]["low"])

        myDict = { "Timestamp": timestamp, "price": price, "Absolute change": change, "High": high, "low": low }
        x = mycol.insert_one(myDict)
        
        #MONGODB
