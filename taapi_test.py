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


def _buyBitcoin(buy_size,pub_key, priv_key):
    # Set up a buy for 0.999 times the current price add more decimals for a higher price and faster fill, if the price is too close to spot your order won't post. 
    # Lower factor makes the order cheaper but fills quickly (0.5 would set an order for half the price and so your order could take months/years/never to fill)
    trader = gemini.PrivateClient(pub_key, priv_key)
    symbol_spot_price = float(trader.get_ticker(symbol)['ask'])
    print(symbol_spot_price)
    factor = 0.999
    #to set a limit order at a fixed price (ie. $55,525) set execution_price = "55525.00" or execution_price = str(55525.00)
    execution_price = str(round(symbol_spot_price*factor,quote_currency_price_increment))

    #set amount to the most precise rounding (tick_size) and multiply by 0.999 for fee inclusion - if you make an order for $20.00 there should be $19.98 coin bought and $0.02 (0.10% fee)
    amount = round((buy_size*0.999)/float(execution_price),tick_size)
        
    #execute maker buy with the appropriate symbol, amount, and calculated price
    buy = trader.new_order(symbol, str(amount), execution_price, "buy", ["maker-or-cancel"])
    print(f'Maker Buy: {buy}')

#Free Taapi Key is rate limited to 1 request every 15 seconds
print(get_rsi())
Event().wait(16)
print(get_cci())
Event().wait(16)
print(get_williams())

if get_rsi() < 30:
    _buyBitcoin(buy_size, gemini_public_key, gemini_private_key)

