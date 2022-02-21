# RSI-CMWilliams-TradingStrategy
 Code to execute the RSI-CMWilliams Trading Strategy on Gemini

Script uses default thresholds from TradingView and Taapi Indicator Data (used to predict local minimums in price with confidence of upcoming 3% rally) to place limit buy orders close to spot BTCUSD on Gemini and opens a limit sell for 3% higher than the spot price of BTCUSD.

Taapi: https://taapi.io/
