import datetime
import requests
import time    
from pymongo import MongoClient
import os
from config import Config

class CurrencyData():
    def __init__(self, currency):
        self.currency = currency
        self.timestamp = datetime.datetime.now(datetime.timezone.utc)
        self.market_cap = None      # nomics, alphavantage

        # Volume in 24 hours
        self.volume = None          # nomics, kraken, alphavantage

        # Circulating supply
        self.supply = None          # nomics

        self.all_time_high = None   # nomics

        # self.all_time_low = None  # all time low doesn't really make sense

        self.high = None            # kraken
        self.low = None             # kraken
        self.open = None            # alphavantage
        self.close = None           # alphavantage

        # Price now X?
        self.price = None           # nomics, coinbase
        self.percent_return = None  # kraken
        self.dollar_return = None   # kraken

    def call_coinbase(self):
        try:
            response = requests.get("https://api.coinbase.com/v2/prices/{}-USD/buy".format(self.currency))
            response.raise_for_status()
            self.price = float(response.json()["data"]["amount"])
        except Exception as e:
            print("Coinbase error")
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
            timeStamp = datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(1), '%Y-%m-%d')
            data = data["Time Series (Digital Currency Daily)"][f"{datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(1), '%Y-%m-%d')}"]

            self.open = float(data["1a. open (USD)"])
            self.close = float(data["4a. close (USD)"])
            self.volume = float(data["5. volume"])
            self.market_cap = float(data["6. market cap (USD)"])
        
        except Exception as e:
            print("Alpha Vantage error")
            print(e)
            
    def call_kraken(self):
        try:
            headers = {"X-CW-API-Key": Config.API_KEYS["CRYPTOWATCH"]}
            url = "https://api.cryptowat.ch/markets/kraken/{}usd/summary".format(self.currency)
            response = requests.request("GET", url, headers=headers)
            response.raise_for_status()
            json_result = response.json()

            # note that this is summary for only one exchange
            self.dollar_return = float(json_result["result"]["price"]["change"]["absolute"])
            self.percent_return = float(json_result["result"]["price"]["change"]["percentage"])
            self.high = float(json_result["result"]["price"]["high"])
            self.low = float(json_result["result"]["price"]["low"])

        except Exception as e:
            print("Kraken error")
            print(e)

    def call_nomics(self):
        # note that this API can call multiple currencies at once
        # so we might want to convert to static method to call all currencies at once later
        try:
            parameters = {"key": Config.API_KEYS["NOMICS"], "ids": self.currency, "interval": "1d"}
            url = "https://api.nomics.com/v1/currencies/ticker"
            response = requests.request("GET", url, parameters=parameters)
            response.raise_for_status()

            # list of one currency
            json_result = response.json()[0]

            self.price = json_result["price"]
            self.market_cap = json_result["market_cap"]
            self.supply = json_result["circulating_supply"]
            self.all_time_high = json_result["high"]

        except Exception as e:
            print("Nomics error")
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

    data_dict = {}

    # Iterator over the APIs that only return data for one currency at a time
    for currency in currencies:
        currency_data = CurrencyData(currency)

        # currency_data.call_coinbase()
        currency_data.call_alphavantage()
        currency_data.call_kraken()

        data_dict[currency] = currency_data
        
    for currency, currency_data in data_dict.items():
        # Use current time
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        myDict = {
            "timestamp": currency_data.timestamp, 
            "price": currency_data.price, 
            "absolute change": currency_data.dollar_return, 
            "percent change": currency_data.percent_return,
            "high": currency_data.high, 
            "low": currency_data.low,
            "all time high": currency_data.all_time_high,
            "supply": currency_data.supply,
            "market cap": currency_data.market_cap,
            "volume": currency_data.volume,
            "open": currency_data.open,
            "close": currency_data.close
        }
        mycol = db[currency]
        x = mycol.insert_one(myDict)

if __name__ == "__main__":
    on_trigger(None, None)
