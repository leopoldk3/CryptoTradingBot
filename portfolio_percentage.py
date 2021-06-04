import websocket, json, pprint, talib, numpy, time, os
import config, webscraping #, tradingprogram
from datetime import datetime
from binance.client import Client
#from binance.websockets import ThreadedWebsocketManager
from binance.enums import *

client = Client(config.api_key, config.api_secret)

percent = input("Please enter the percentage growth you want before selling. Just the number: ")

#allows for a dictionary to be inputed and you can access keys of the dictionary by creating an instance of the object and then instance.key will give the value under the key
class objectview(object):
    def __init__(self,d):
        self.__dict__ = d

#make so everytime the function recurrs itself it adds the portfolio value and time of value to the list. 
total_portfolio_values = []
#if asset shows up on the top 5 or used before append it to this list
assets_traded = ['XRP', 'ETH', 'BTC', 'USDT']

def get_portfolio_value():
    assets_with_value = []
    portfolio_value = 0
    #For each asset in assets_traded, it gets the returned dictionary and if it has value then it adds the asset to an assets_with_value list
    for ticker in assets_traded:
        o = objectview(client.get_asset_balance(asset=ticker))
        if float(o.free) > 0:
            #print("{} of {} held.".format(o.free, o.asset))
            assets_with_value.append(o.asset)
        elif float(o.free) <= 0:
            #print("No {} positions held.".format(o.asset))
            pass
        else:
            print("error")
    #for each asset with a value will convert the current avg price to usdt 
    for ticker in assets_with_value:
        o = objectview(client.get_asset_balance(asset=ticker))
        symbol = '{}USDT'.format(ticker)
        price = client.get_avg_price(symbol= symbol)
        usdt_value = float(o.free) * float(price["price"])
        portfolio_value += usdt_value

    #print("Estimated portfolio value in USDT is: ${}".format(portfolio_value))
    return portfolio_value

#order function with quantity in USDT
def order_qQQ(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quoteOrderQty = quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

#order function with quanity in crypto
def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

def percentage_portfolio(percent):

    #This sets the end time as 6 hours after first calling upon it 
    t_end = time.time() + 60 * 60 * 6

    #adds dictionary of date and time and the current portfolio value to the toal portfolio global list
    portfolio_timestamped = {
        "Date_and_Time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Value_USDT": get_portfolio_value()
    }
    total_portfolio_values.append(portfolio_timestamped)

    #gets the total portfolio value of a portfolio gaining "percent" growth from its current value 
    latest_portfolio_dict = total_portfolio_values[-1]
    needed_gain = (latest_portfolio_dict["Value_USDT"]/float(100))*(float(percent))
    projected_portfolio_value = latest_portfolio_dict["Value_USDT"] + needed_gain

    #lists top 5 moving (gaining) cryptos
    top5 = webscraping.get_top_five_gainers()

    #amount in USDT to allocate for each currency
    USDT_trade_amount = latest_portfolio_dict["Value_USDT"]/5

    #list of held cryptos during the 6 hr period
    cryptos_holding = []

    #while within 6 hours from the start of the period 
    while (time.time() < t_end):
        #while the portfilio value is less than the projected 
        while (get_portfolio_value() < projected_portfolio_value):
            #for each of the top 5 gaining cryptos it buys it if not already holding during this period
            for ticker in top5: 
                if ticker not in cryptos_holding:
                    symbol = '{}USDT'.format(ticker)
                    price = client.get_avg_price(symbol= symbol)
                    ticker_trade_amount = USDT_trade_amount/float(price["price"])
                    # binance BUY order logic here
                    order_succeeded = order_qQQ(SIDE_BUY, str(USDT_trade_amount), symbol)
                    if order_succeeded:
                        cryptos_holding.append(ticker)
                        if ticker not in assets_traded:
                            assets_traded.append(ticker)
                        print("BOUGHT {},{}.".format(ticker_trade_amount, ticker))
                    if order_succeeded == False:
                        print("Error buying {}. Possibly not enough funds".format(symbol))
                        break

                elif ticker in cryptos_holding:
                    pass
        #for each ticker held it sells back to usdt after the portfolio has increased by the percent
        for ticker in cryptos_holding:
            o = objectview(client.get_asset_balance(asset=ticker))
            symbol = '{}USDT'.format(ticker)
            # binance SELL logic here
            order_succeeded = order(SIDE_SELL, float(o.free), symbol)
            if order_succeeded:
                cryptos_holding.remove(ticker)
                print("SOLD {},{}.".format(float(o.free), ticker))
    #sells remaining positions if portfolio did not go up percentage over the period
    for ticker in cryptos_holding:
        o = objectview(client.get_asset_balance(asset=ticker))
        symbol = '{}USDT'.format(ticker)
        # binance SELL logic here
        order_succeeded = order(SIDE_SELL, float(o.free), symbol)
        if order_succeeded:
            cryptos_holding.remove(ticker)
            print("SOLD {},{}.".format(float(o.free), ticker))
    
    portfolio_change = get_portfolio_value() - latest_portfolio_dict["Value_USDT"]
    print("The portfolio changed ${} USDT over the period.".format(portfolio_change))
    percentage_portfolio(percent)

percentage_portfolio(percent)