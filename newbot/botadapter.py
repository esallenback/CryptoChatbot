from chatterbot.logic import LogicAdapter

class PriceAdapter(LogicAdapter):
    import requests

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

    
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['what', 'is', 'price', 'of']
        #print("hello can_process")


        if all(x in statement.text.split() for x in words):
            print(x)
            for y in statement.text.split():
                if cryptoDict.get(x):
                    return True

        return False

    def process(self, input_statement):
        from chatterbot.conversation import Statement
        #get the crypto in question
        confidence = 0
        output_response = Statement(text='')
        #print("Hello chat process")
        for x in input_statement.text.split():
            if cryptoDict.get(x):
                
                retrievePrice = float(requests.get("https://api.coinbase.com/v2/prices/" + cryptoDict.get(x) + "-USD/buy").json()["data"]["amount"])
                
                if retrievePrice:
                    confidence = 1
                    output_string = "Current price of " + x + ": $" + string(retrievePrice)
                    output_response = Statement(text=output_string)
                    return confidence, output_resposne
        return confidence, output_resposne
            
