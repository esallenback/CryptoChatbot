import parserr
import cryptobot as cb
import datetime
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        return render_template('webpage.html') + process() + '<br><br>' + 'Real time data taken from coinbase.com'
    else:
        return render_template('webpage.html') + '<br><br>' + 'Real time data taken from coinbase.com'
    
def priceOf(cryptoName, cryptoType):
    return ("Current price of " + cryptoName + ": " +
            str(float(requests.get("https://api.coinbase.com/v2/prices/" + cryptoType + "-USD/buy").json()["data"]["amount"])))

def cryptoIntro():
    return ("'A cryptocurrency is a digital or virtual currency that is secured by cryptography, \n" +
        "which makes it nearly impossible to counterfeit or double-spend. Many cryptocurrencies \n" +
        "are decentralized networks based on blockchain technology—a distributed ledger enforced \n" +
        "by a disparate network of computers. A defining feature of cryptocurrencies is that they \n" +
        "are generally not issued by any central authority, rendering them theoretically immune \n" +
        "to government interference or manipulation.' - Investopedia")

def absoluteCrypto(cryptoName, cryptoType):
    url = "https://api.cryptowat.ch/markets/kraken/" + cryptoType + "usd/summary"

    response = requests.request("GET", url)
    try:
        return ("Change in " + cryptoName + " (24hrs): " +
              str(response.json()["result"]["price"]["change"]["absolute"]))
    except:
        return "Cannot retrieve change in currency over 24 hrs for " + cryptoName

def percentCrypto(cryptoName, cryptoType):
    url = "https://api.cryptowat.ch/markets/kraken/" + cryptoType + "usd/summary"

    response = requests.request("GET", url)
    try:
        return ("Percent change for " + cyrptoName + "(24hrs): " +
              str(response.json()["result"]["price"]["change"]["percent"]))
    except:
        return "Cannot retrieve percent change in currency for " + cryptoName

def highCrypto(cryptoName, cryptoType):
    url = "https://api.cryptowat.ch/markets/kraken/" + cryptoType + "usd/summary"

    response = requests.request("GET", url)
    try:
        return ("High for " + cryptoName + " for the day: " +
              str(response.json()["result"]["price"]["high"]))
    except:
        return "Cannot retrieve high for the day for " + cryptoName

def lowCrypto(cryptoName, cryptoType):
    url = "https://api.cryptowat.ch/markets/kraken/" + cryptoType + "usd/summary"

    response = requests.request("GET", url)
    try:
        return ("Low for " + cryptoName + " for the day: " +
              str(response.json()["result"]["price"]["low"]))
    except:
        return "Cannot retrieve low for the day for " + cryptoName

def openCrypto(cryptoName, cryptoType):
    url = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=" + cryptoType + "&market=USD&apikey=729WZLMQLLZMCYJF"
    try:
        return ("The open for the day in USD for " + cryptoName + " is " +
              str((requests.request("GET", url)).json()["Time Series (Digital Currency Daily)"][f"{datetime.datetime.now():%Y-%m-%d}"]["1a. open (USD)"]))
    except:
        return "Cannot retrieve open for the day for " + cryptoName

def closeCrypto(cryptoName, cryptoType):
    url = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=" + cryptoType + "&market=USD&apikey=729WZLMQLLZMCYJF"
    try:
        return ("The close for the day in USD for " + cryptoName + " is " +
            str((requests.request("GET", url)).json()["Time Series (Digital Currency Daily)"][f"{datetime.datetime.now():%Y-%m-%d}"]["4a. close (USD)"]))
    except:
        return "Cannot retrieve close for the day for " + cryptoName


def volumeCrypto(cryptoName, cryptoType):
    url = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=" + cryptoType + "&market=USD&apikey=729WZLMQLLZMCYJF"
    try:
        return ("The volume for " + cryptoName + " over the last 24 hours is " +
            str((requests.request("GET", url)).json()["Time Series (Digital Currency Daily)"][f"{datetime.datetime.now():%Y-%m-%d}"]["5. volume"]))
    except:
        return "Cannot retrieve volume over the past 24 hours for " + cryptoName

def marketCap(cryptoName, cryptoType):
    url = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=" + cryptoType + "&market=USD&apikey=729WZLMQLLZMCYJF"
    try:
        return ("The market cap for " + cryptoName + " in USD is " +
            str((requests.request("GET", url)).json()["Time Series (Digital Currency Daily)"][f"{datetime.datetime.now():%Y-%m-%d}"]["6. market cap (USD)"]))
    except:
        return "Cannot retrieve market cap for " + cryptoName

def aboutCrypto(cryptoName):
    cryptoAbout = dict({"BTC": "The world’s first cryptocurrency, Bitcoin is stored and exchanged securely on the internet through a digital ledger known as a blockchain. Bitcoins are divisible into smaller units known as satoshis — each satoshi is worth 0.00000001 bitcoin.",
                         "ETH": "Ethereum is both a cryptocurrency and a decentralized computing platform. Developers can use the platform to create decentralized applications and issue new crypto assets, known as Ethereum tokens.",
                         "LTC": "Litecoin is a cryptocurrency that uses a faster payment confirmation schedule and a different cryptographic algorithm than Bitcoin.",
                         "DAI": "Dai (DAI) is a decentralized stablecoin running on Ethereum (ETH) that attempts to maintain a value of $1.00 USD. Unlike centralized stablecoins, Dai isn't backed by US dollars in a bank account. Instead, it’s backed by collateral on the Maker platform.",
                         "EOS": "EOS is a cryptocurrency designed to support large-scale applications. There are no fees to send or receive EOS. Instead, the protocol rewards the entities that run the network periodically with new EOS, effectively substituting inflation for transaction fees.",
                         "XLM": "Stellar’s cryptocurrency, the Stellar Lumen (XLM), powers the Stellar payment network. Stellar aims to connect banks, payment systems, and individuals quickly and reliably.",
                         "XRP": "XRP is the cryptocurrency used by the Ripple payment network. Built for enterprise use, XRP aims to be a fast, cost-efficient cryptocurrency for cross-border payments.",
                         "LINK": "Chainlink (LINK) is an Ethereum token that powers the Chainlink decentralized oracle network. This network allows smart contracts on Ethereum to securely connect to external data sources, APIs, and payment systems.",
                         "DASH": "Dash is a cryptocurrency with optional speed and privacy features. Its unique network architecture consists of both regular miners and privileged machines called Masternodes.",
                         "XTZ": "Tezos is a cryptocurrency and decentralized computing platform. Its features include proof of stake consensus, formal verification (which lets developers verify the correctness of their code), and the ability to let stakeholders vote on changes to the protocol.",
                         "BAT": "The Basic Attention Token (BAT) is an ethereum-based token that is deigned to improve digital advertising on the web.",
                         "ZEC": "Zcash is a cryptocurrency that offers two types of addresses: transparent addresses that are publicly visible on the Zcash blockchain and shielded addresses that are more private.",
                         "ZRX": "ZRX is an Ethereum token that is used to power the 0x protocol. The protocol itself is designed to allow Ethereum tokens to be traded at a low cost directly from your wallet.",
                         "REP": "Augur’s Reputation token (REP) is an Ethereum token designed for reporting and disputing the outcome of events on online prediction markets. Reporters are rewarded for reporting the outcome of events correctly."})
    print(cryptoAbout.get(cryptoName) + " - coinbase.com")

def process():
    query = request.form['user_input']
    cryptoDict = dict({"bitcoin": "BTC",
                       "btc": "BTC",
                       "ethereum": "ETH",
                       "eth": "ETH",
                       "litecoin": "LTC",
                       "ltc": "LTC",
                       "dai": "DAI",
                       "eos": "EOS",
                       "stellar": "XLM",
                       "xlm": "XLM",
                       "bat": "BAT",
                       "ripple": "XRP",
                       "xrp": "XRP",
                       "chainlink": "LINK",
                       "link": "LINK",
                       "dash": "DASH",
                       "tezos": "XTZ",
                       "xtz": "XTZ",
                       "zcash": "ZEC",
                       "zec": "ZEC",
                       "ox": "ZRX",
                       "zrx": "ZRX",
                       "augur": "REP",
                       "rep": "REP"})
    # takes in input from command line
    
    parsed_query = parserr.parse(query)[0]
    cryptos = parserr.parse(query)[1]

    response = cb.respond(parsed_query)

    if parserr.unparse(response, cryptos) == "off-topic":
        print("off topic")
    if len(response) != 0:
        question = response[0]
        crypto = parserr.unparse(response, cryptos).strip()
        # DEBUG:
        # print(question, crypto)
        # print("~"+crypto+"~")
        if cryptoDict.get(crypto) != None:
            if question == "price":
                return priceOf(crypto, cryptoDict.get(crypto))
            elif question == "cryptointro":
                return cryptoIntro()
            elif question == "close":
                return closeCrypto(crypto, cryptoDict.get(crypto))
            elif question == "opens":
                return openCrypto(crypto, cryptoDict.get(crypto))
            elif question == "high":
                return highCrypto(crypto, cryptoDict.get(crypto))
            elif question == "low":
                return lowCrypto(crypto, cryptoDict.get(crypto))
            elif question == "percent":
                return percentCrypto(crypto, cryptoDict.get(crypto))
            elif question == "absolute":
                return absoluteCrypto(crypto, cryptoDict.get(crypto))
            elif question == "volume":
                return volumeCrypto(crypto, cryptoDict.get(crypto))
            elif question == "about":
                return aboutCrypto(cryptoDict.get(crypto))
            elif question == "marketcap":
                return marketCap(crypto, cryptoDict.get(crypto))
            else:
                return "I cannot answer that right now"
        else:
            return "I'm not trained to answer that question."
    else:
        return "Off topic"
if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(debug=True,port=5002)
