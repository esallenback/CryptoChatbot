import datetime
import requests
import time    
from pymongo import MongoClient
import os
from config import Config

class CurrencyData():
    def __init__(self, currency):
        self.currency = currency
        self.date = datetime.datetime.now()
        self.market_cap = None

        # Volume in 24 hours
        self.volume = None

        # Circulating supply
        self.supply = None
        self.all_time_high = None
        self.all_time_low = None
        self.high = None
        self.low = None

        # Price now X?
        self.price = None
        self.percent_return = None
        self.dollar_return = None

    def call_coinbase(self):
        try:
            response = requests.get("https://api.coinbase.com/v2/prices/{}-USD/buy".format(self.currency))
            response.raise_for_status()
            self.price = float(response.json()["data"]["amount"])
        except Exception as e:
            print(e)

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
        currency_data = CurrencyData()

        currency_data.call_coinbase()
        
        # Does not work - need account or API key?
        headers = {"X-CW-API-Key": Config.API_KEYS["CRYPTOWATCH"]}
        url = "https://api.cryptowat.ch/markets/kraken/{}usd/summary".format(currency)
        response = requests.request("GET", url, headers=headers)
        
        #Absolute change in crypto
        change = str(response.json()["result"]["price"]["change"]["absolute"])

        #Percent change in crypto
        #print("Percent change for " + currencies[i] + "(24hrs): " +
        #          str(response.json()["result"]["price"]["change"]["percent"]))
        
        #High for crypto
        high = str(response.json()["result"]["price"]["high"])
        
        #Low for crypto
        low = str(response.json()["result"]["price"]["low"])

        # timestamp is 12/02/2019 @ 2:30pm (UTC) - why are we using this date?
        timestamp = datetime.datetime.fromtimestamp(1575297000).isoformat()

        # Why are values inserted as strings into the database?
        myDict = { "Timestamp": timestamp, "price": price, "Absolute change": change, "High": high, "low": low }
        mycol = db[currency]
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
