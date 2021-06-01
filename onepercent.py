import websocket, json, pprint, talib, numpy, datetime
import config, webscraping, tradingprogram
from binance.client import Client
from binance.enums import *

client = Client(config.API_KEY, config.API_SECRET, tld='us')
percent = input("Please enter the percentage growth you want before selling. Just the number.")

#strip this to only give the time
time= datetime.now()

total_portfolio_values = [{'value': time}] 


#type in currency ticker all caps and no spaces 
trade_currency = input("Please enter currency you want to trade:")

# candle sticks are every 1 min because at the end of the stream it is @kline_1m can change if wanted
SOCKET = ("wss://stream.binance.com:9443/ws/{}usdt@kline_1m").format(trade_currency.lower())

TRADE_SYMBOL = '{}USD'.format(trade_currency)
