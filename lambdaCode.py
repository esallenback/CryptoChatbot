from datetime import datetime, time, timedelta, timezone
import math
import requests
import time    
from pymongo import MongoClient
import os
from config import Config

class CurrencyData():
    def __init__(self, currency, time=datetime.combine(datetime.utcnow().date(), time.min()).replace(tzinfo=timezone.utc)):
        self.currency = currency

        # Get yesterday's data
        #self.timestamp = datetime.now(timezone.utc) - timedelta(days=1)
        #self.timestamp = self.timestamp.replace(hour=0, minute=0, second=0, microsecond=0)

        # Defaults to midnight of today (in the morning)
        self.timestamp = math.floor(time)
        
        self.market_cap = None      # nomics

        # Volume in 24 hours
        self.volume = None

        # Circulating supply
        self.supply = None          # nomics

        self.all_time_high = None   # nomics

        self.high = None
        self.low = None
        self.open = None
        self.close = None

        # Price now X?
        # Price at what time?
        # self.price = None
        self.percent_return = None  # kraken
        self.dollar_return = None   # kraken

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
            timeStamp = datetime.strftime(datetime.now(timezone.utc) - timedelta(1), '%Y-%m-%d')
            data = data["Time Series (Digital Currency Daily)"][f"{datetime.strftime(datetime.now(timezone.utc) - timedelta(1), '%Y-%m-%d')}"]

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
            response = requests.request("GET", url, params=parameters)
            response.raise_for_status()

            # list of one currency
            json_result = response.json()[0]

            # self.price = json_result["price"]
            self.market_cap = float(json_result["market_cap"])
            self.supply = float(json_result["circulating_supply"])
            self.all_time_high = float(json_result["high"])

        except Exception as e:
            print("Nomics error")
            print(e)

    def call_coinapi(self):
        try:
            url = "https://rest.coinapi.io/v1/ohlcv/{}/USD/history".format(self.currency)
            parameters = {"period_id": "1DAY", "time_start": self.timestamp.isoformat(), "limit": 1}
            headers = {'X-CoinAPI-Key' : Config.API_KEYS["COINAPI"]}
            response = requests.request("GET", url, params=parameters, headers=headers)
            response.raise_for_status()

            print(response.text)

        except Exception as e:
            print("Coinapi error")
            print(e)

    def call_cryptocompare(self):
        # Be sure to run at the correct time UTC
        try:
            headers = {"Apikey": Config.API_KEYS["CRYPTOCOMPARE"]}

            url = "https://min-api.cryptocompare.com/data/v2/histoday"
            parameters = {"fsym": self.currency, "tsym": "USD", "limit": 1, "toTS": self.timestamp.timestamp()}
            response = requests.request("GET", url, params=parameters, headers=headers)

            data = response.json()["Data"]["Data"][0]

            self.open = float(data["open"])
            self.close = float(data["close"])
            self.high = float(data["high"])
            self.low = float(data["low"])

            self.dollar_return = self.close - self.open
            self.percent_return = self.dollar_return / self.open * 100

            url = "https://min-api.cryptocompare.com/data/symbol/histoday"
            parameters = {"fsym": self.currency, "tsym": "USD", "limit": 1}
            response = requests.request("GET", url, params=parameters, headers=headers)

            self.volume = float(response.json()["Data"][0]["total_volume_total"])

        except Exception as e:
            print("Cryptocompare error")
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

        currency_data.call_nomics()
        currency_data.call_cryptocompare()

        data_dict[currency] = currency_data
        
    for currency, currency_data in data_dict.items():
        myDict = {
            "timestamp": currency_data.timestamp, 
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
