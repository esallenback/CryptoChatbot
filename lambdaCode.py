import datetime
import requests
import time    
from pymongo import MongoClient
import os
from config import Config

class CurrencyData():
    def __init__(self, currency):
        self.currency = currency
        self.timestamp = datetime.datetime.now()
        self.market_cap = None      # alphavantage

        # Volume in 24 hours
        self.volume = None          # alphavantage, kraken

        # Circulating supply
        self.supply = None

        self.all_time_high = None
        self.all_time_low = None
        self.high = None            # kraken
        self.low = None             # kraken
        self.open = None            # alphavantage
        self.close = None           # alphavantage

        # Price now X?
        self.price = None           # coinbase
        self.percent_return = None  # kraken?
        self.dollar_return = None   # kraken?

    def call_coinbase(self):
        try:
            response = requests.get("https://api.coinbase.com/v2/prices/{}-USD/buy".format(self.currency))
            response.raise_for_status()
            self.price = float(response.json()["data"]["amount"])
        except Exception as e:
            print(e)

    def call_alphavantage(self):
        try:
            # Note that this API only allows 5 calls per minute and 500 calls per day on free plan
            # Perhaps update to premium account at https://www.alphavantage.co/premium/
            payload = {"function": "DIGITAL_CURRENCY_DAILY", "symbol": self.currency, "market": "USD", "apikey": Config.API_KEYS["ALPHAVANTAGE"]}
            url = "https://www.alphavantage.co/query"
            response = requests.request("GET", url, params=payload)
            response.raise_for_status()

            data = response.json()
            if "Note" in data:
                print(data["Note"])
                return

            #The timestamp is for yesterday (Some of the cryptos are not yet updated - easier to pull data for day before)
            timeStamp = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')
            data = data["Time Series (Digital Currency Daily)"][f"{datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')}"]

            self.open = float(data["1a. open (USD)"])
            self.close = float(data["4a. close (USD)"])
            self.volume = float(data["5. volume"])
            self.market_cap = float(data["6. market cap (USD)"])
        
        except Exception as e:
            print(e)
            
    def call_kraken(self):
        try:
            headers = {"X-CW-API-Key": Config.API_KEYS["CRYPTOWATCH"]}
            url = "https://api.cryptowat.ch/markets/kraken/{}usd/summary".format(currency)
            response = requests.request("GET", url, headers=headers)
            response.raise_for_status()

            #Absolute change in crypto
            self.dollar_return = float(response.json()["result"]["price"]["change"]["absolute"])

            #Percent change in crypto
            self.percent_return = float(response.json()["result"]["price"]["change"]["percent"])
            
            self.high = str(response.json()["result"]["price"]["high"])
            self.low = str(response.json()["result"]["price"]["low"])

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
        currency_data = CurrencyData(currency)

        currency_data.call_coinbase()
        currency_data.call_alphavantage()
        # currency_data.call_kraken()
        
        # timestamp is 12/02/2019 @ 2:30pm (UTC) - why are we using this date?
        timestamp = datetime.datetime.fromtimestamp(1575297000).isoformat()

        # Why are values inserted as strings into the database?
        myDict = {
            "Timestamp": currency_data.timestamp, 
            "price": currency_data.price, 
            "Absolute change": currency_data.change, 
            "High": currency_data.high, 
            "low": currency_data.low
        }
        mycol = db[currency]
        x = mycol.insert_one(myDict)

if __name__ == "__main__":
    on_trigger(None, None)
