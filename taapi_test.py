import json
import gemini
import requests 
from threading import Event

#API Keys
gemini_public_key = ""  
gemini_private_key = ""
taapi_key=""

#Indicator Variables - based on default values from TradingView. You can update these if you want a more conservative / aggressive strategy.
RSI_FLOOR = 30
CCI_FLOOR = -200
WILLIAMS_FLOOR = -80

#Taapi Variables
RSI_SYMBOL = "BTC/USDT"
RSI_INTERVAL = "15m"
BASE_URL = "https://api.taapi.io/"
AUTH_URL = "?secret="+taapi_key+"&exchange=binance&symbol="+RSI_SYMBOL+"&interval="+RSI_INTERVAL
RSI_URL = "rsi"
CCI_URL = "cci"
WILLIAMS_URL = "willr"

#Gemini Variables
symbol = "BTCUSD"
tick_size = 8
quote_currency_price_increment = 2
buy_size = 10

def get_rsi():
    response = requests.get(BASE_URL+RSI_URL+AUTH_URL)
    print(response)
    json_data = json.loads(response.text)
    rsi_value = json_data['value']
    print(f"RSI Value is {rsi_value}")
    return rsi_value

def get_cci():
    response = requests.get(BASE_URL+CCI_URL+AUTH_URL)
    print(response)
    json_data = json.loads(response.text)
    cci_value = json_data['value']
    print(f"CCI Value is {cci_value}")
    return cci_value

def get_williams():
    response = requests.get(BASE_URL+WILLIAMS_URL+AUTH_URL)
    print(response)
    json_data = json.loads(response.text)
    williams_value = json_data['value']
    print(f"Williams Value is {williams_value}")
    return williams_value

#Places limit buy order for 0.999 times the current spot price. Needs to be limit order so we can get lowest fee execution. Should fill quickly most of the time, for faster fills increase the factor closer to 1. Can't be 1 though becaasue then the order won't fill as maker.
def _buyBitcoin(buy_size,pub_key, priv_key):
    trader = gemini.PrivateClient(pub_key, priv_key)
    symbol_spot_price = float(trader.get_ticker(symbol)['ask'])
    print(symbol_spot_price)
    factor = 0.999
    execution_price = str(round(symbol_spot_price*factor,quote_currency_price_increment))
    amount = round((buy_size*0.999)/float(execution_price),tick_size)
    buy = trader.new_order(symbol, str(amount), execution_price, "buy", ["maker-or-cancel"])
    print(f'Maker Buy: {buy}')
    return amount

#Places limit sell order for 3% higher than the spot price of BTC. Change factor variable for different percentage
def _sellBitcoin(sell_size,pub_key, priv_key):
    trader = gemini.PrivateClient(pub_key, priv_key)
    symbol_spot_price = float(trader.get_ticker(symbol)['ask'])
    factor = 1.03
    execution_price = str(round(symbol_spot_price*factor,2))
    sell = trader.new_order(symbol, str(sell_size), execution_price, "sell", ["maker-or-cancel"])
    print(f'Maker Sell: {sell}')

def lambda_handler(event, context):
    #Free Taapi Key is rate limited to 1 request every 15 seconds
    rsi = get_rsi()
    Event().wait(16)
    cci = get_cci()
    Event().wait(16)
    williams = get_williams()
        
    if rsi < RSI_FLOOR and cci < CCI_FLOOR and williams < WILLIAMS_FLOOR:
        btc_bought = _buyBitcoin(buy_size, gemini_public_key, gemini_private_key)
        _sellBitcoin(btc_bought, gemini_public_key, gemini_private_key)
        print("Order's posted")
        print(f"RSI: {rsi}")
        print(f"CCI: {cci}")
        print(f"Williams: {williams}")
    else:
        print("RSI, CCI, Williams Indicators not met")
        print(f"RSI: {rsi}")
        print(f"CCI: {cci}")
        print(f"Williams: {williams}")

    return {
        'statusCode': 200,
        'body': json.dumps('End of script')
    }