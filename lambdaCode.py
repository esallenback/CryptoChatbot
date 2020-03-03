import datetime
import requests
import time    
from pymongo import MongoClient
import os
from config import Config

def on_trigger(event, context):
    #connectionString = os.environ["MONGO_URL"]

    currencies = ['BTC', 'ETH',
            'LTC', 'DAI',
            'EOS', 'XLM',
            'BAT', 'XRP',
            'LINK', 'DASH',
            'XTZ', 'ZEC', 'REP']

    client = MongoClient("mongodb+srv://emilys:UIUCchatbot@cluster0-ar3em.mongodb.net/test?retryWrites=true&w=majority")
    db = client["cryptocurrencyChatbot"]

    # Iterating the index 
    # same as 'for i in range(len(currencies))' 
    for currency in currencies:
        mycol = db[currency]
        #time.sleep(10)
        
        #Price of crypto
        # timestamp is 12/02/2019 @ 2:30pm (UTC)
        timestamp = datetime.datetime.fromtimestamp(1575297000).isoformat()
        price = str(float(requests.get("https://api.coinbase.com/v2/prices/{}-USD/buy".format(currency))
            .json()["data"]["amount"]))
        
        # Does not work - need account or API key?
        payload = {"apikey": Config.API_KEYS["CRYPTOWATCH"]}
        url = "https://api.cryptowat.ch/markets/kraken/{}usd/summary".format(currency)
        response = requests.request("GET", url, params=payload)
        
        #Absolute change in crypto
        change = str(response.json()["result"]["price"]["change"]["absolute"])

        #Percent change in crypto
        #print("Percent change for " + currencies[i] + "(24hrs): " +
        #          str(response.json()["result"]["price"]["change"]["percent"]))
        
        #High for crypto
        high = str(response.json()["result"]["price"]["high"])
        
        #Low for crypto
        low = str(response.json()["result"]["price"]["low"])

        # Why are values inserted as strings into the database?
        myDict = { "Timestamp": timestamp, "price": price, "Absolute change": change, "High": high, "low": low }
        x = mycol.insert_one(myDict)
        
        # Note that this API only allows 5 calls per minute and 500 calls per day on free plan
        # Perhaps update to premium account at https://www.alphavantage.co/premium/
        payload = {"function": "DIGITAL_CURRENCY_DAILY", "symbol": currency, "market": "USD", "apikey": Config.API_KEYS["ALPHAVANTAGE"]}
        url = "https://www.alphavantage.co/query"
        response = requests.request("GET", url, params=payload)
        
        try:

            if (response.status_code == 200):
            
                #The timestamp is for yesterday (Some of the cryptos are not yet updated - easier to pull data for day before)
                timeStamp = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')

                data = response.json()["Time Series (Digital Currency Daily)"][f"{datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')}"]
                
                #Open for crypto
                print(str(data["1a. open (USD)"]))

                #Close for crypto
                print(str(data["4a. close (USD)"]))

                #Volume for crypto
                print(str(data["5. volume"]))

                #Market Cap for crypto
                print(str(data["6. market cap (USD)"]))
                
        except:
            print("Status Code {}: {}".format(response.status_code, response.text))
            
        print("___________________________________")

if __name__ == "__main__":
    on_trigger(None, None)
