import datetime
import requests
import time    
from pymongo import MongoClient
import os

def on_trigger(event, context):
    #connectionString = os.environ["MONGO_URL"]

    currencies = ['BTC', 'ETH',
            'LTC', 'DAI',
            'EOS', 'XLM',
            'BAT', 'XRP',
            'LINK', 'DASH',
            'XTZ', 'ZEC', 'REP']
    num_currencies = len(currencies)

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
        
        url = "https://api.cryptowat.ch/markets/kraken/usd/summary".format(currency)
        response = requests.request("GET", url)
        
        #Absolute change in crypto
        change = str(response.json()["result"]["price"]["change"]["absolute"])

        #Percent change in crypto
        #print("Percent change for " + currencies[i] + "(24hrs): " +
        #          str(response.json()["result"]["price"]["change"]["percent"]))
        
        #High for crypto
        high = str(response.json()["result"]["price"]["high"])
        
        #Low for crypto
        low = str(response.json()["result"]["price"]["low"])

        myDict = { "Timestamp": timestamp, "price": price, "Absolute change": change, "High": high, "low": low }
        x = mycol.insert_one(myDict)
        
        #MONGODB
        if(False):
            payload = {"function": "DIGITAL_CURRENCY_DAILY", "symbol": currency, "market": "USD", "apikey": "729WZLMQLLZMCYJF"}
            # url = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=" + currency + "&market=USD&apikey=729WZLMQLLZMCYJF"  
            response = requests.request("GET", url, params=payload)
            
            try:

                if (response.status_code == 200):
                
                    #The timestamp is for yesterday (Some of the cryptos are not yet updated - easier to pull data for day before)
                    timeStamp = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')
                    
                    #Open for crypto
                    print(str(response.json()["Time Series (Digital Currency Daily)"][f"{datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')}"]["1a. open (USD)"]))

                    #Close for crypto
                    print(str(response.json()["Time Series (Digital Currency Daily)"][f"{datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')}"]["4a. close (USD)"]))

                    #Volume for crypto
                    print(str(response.json()["Time Series (Digital Currency Daily)"][f"{datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')}"]["5. volume"]))

                    #Market Cap for crypto
                    print(str(response.json()["Time Series (Digital Currency Daily)"][f"{datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')}"]["6. market cap (USD)"]))

                    
            except:
                
                print("Cannot retrieve the data at this time")
                
            print("___________________________________")

if __name__ == "__main__":
    on_trigger(None, None)
