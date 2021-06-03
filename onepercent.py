import websocket, json, pprint, talib, numpy, time
import config, webscraping, tradingprogram
from binance.client import Client
from binance.enums import *

client = Client(config.API_KEY, config.API_SECRET, tld='us')
percent = input("Please enter the percentage growth you want before selling. Just the number.")

#maybe make everything a function so at the end of the 6 hours it calls it again with reccursion and reevelutes everything? 


#This sets the end time as 6 hours after first calling upon it 
t_end = time.time() + 60 * 60 * 6
print (time.time())
print (t_end)

while time.time() < t_end:
    # do whatever you do
    break 

total_portfolio_values = [{'value': time}] 


#type in currency ticker all caps and no spaces 
trade_currency = input("Please enter currency you want to trade:")

# candle sticks are every 1 min because at the end of the stream it is @kline_1m can change if wanted
SOCKET = ("wss://stream.binance.com:9443/ws/{}usdt@kline_1m").format(trade_currency.lower())

TRADE_SYMBOL = '{}USD'.format(trade_currency)
