from chatterbot.logic import LogicAdapter
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

class PriceAdapter(LogicAdapter):


    

    
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['what', 'is', 'price', 'of']

        if all(w in statement.text.lower() for w in words):
            for y in statement.text.split():
                if cryptoDict.get(y.lower()):
                    return True
            
        return False

    def process(self, input_statement, additional_params):
        from chatterbot.conversation import Statement
        import requests
        #get the crypto in question
        response_statement = Statement('bad')
        response_statement.confidence = 0
        for x in input_statement.text.split():
            if cryptoDict.get(x.lower()):
                retrievePrice = float(requests.get("https://api.coinbase.com/v2/prices/" + cryptoDict.get(x.lower()) + "-USD/buy").json()["data"]["amount"])

                if retrievePrice:
                    output_string = "Current price of " + x + ": $" + str(retrievePrice)
                    response_statement = Statement(output_string)
                    response_statement.confidence = 1
        return response_statement
            
