import json
import gemini
import requests 
from threading import Event

gemini_public_key = ""  
gemini_private_key = ""
taapi_key = ""

#Taapi Variables
INCLUDE_RSI = True 
RSI_SYMBOL = "BTC/USDT"
RSI_INTERVAL = "15m"
RSI_FLOOR = 40
BASE_URL = "https://api.taapi.io/"
AUTH_URL = "?secret="+taapi_key+"&exchange=binance&symbol="+RSI_SYMBOL+"&interval="+RSI_INTERVAL
WILLIAMS_URL = "willr"
CCI_URL = "cci"
RSI_URL = "rsi"

#Gemini Variables
symbol = "BTCUSD"
tick_size = 8
quote_currency_price_increment = 2

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

#Places limit sell order for 3% higher than the spot price of BTC. Change factor variable for different percentage
def _sellBitcoin(sell_size,pub_key, priv_key):
    trader = gemini.PrivateClient(pub_key, priv_key)
    symbol_spot_price = float(trader.get_ticker(symbol)['ask'])
    factor = 1.03
    execution_price = str(round(symbol_spot_price*factor,2))
    amount = round((sell_size*.999)/float(price),tick_size)
    sell = trader.new_order(symbol, str(amount), price, "sell", ["maker-or-cancel"])
    print(f'Maker Sell: {sell}')
    return [btc_amount, price]

#Free Taapi Key is rate limited to 1 request every 15 seconds
print(get_rsi())
Event().wait(16)
print(get_cci())
Event().wait(16)
print(get_williams())

if get_rsi() < 30:
    _buyBitcoin(buy_size, gemini_public_key, gemini_private_key)
    _sellBitcoin(sell_size, gemini_public_key, gemini_private_key)

