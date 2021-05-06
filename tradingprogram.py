import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

# candle sticks are every 1 min because at the end of the stream it is @kline_1m can change if wanted

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.05

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET, tld='us')


class RSI_Strategy: 
    def __init__ (self, period, overbought, oversold):
        self.RSI_PERIOD = period
        self.RSI_OVERBOUGHT = overbought
        self.RSI_OVERSOLD = oversold
    def run(self):   
        if len(closes) > self.RSI_PERIOD:
                np_closes = numpy.array(closes)
                rsi = talib.RSI(np_closes, self.RSI_PERIOD)
                print("all rsis calculated so far")
                print(rsi)
                last_rsi = rsi[-1]
                print("the current rsi is {}".format(last_rsi))

                if last_rsi > self.RSI_OVERBOUGHT:
                    if in_position:
                        print("Overbought! Sell! Sell! Sell!")
                        # put binance sell logic here
                        order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                        if order_succeeded:
                            in_position = False
                    else:
                        print("It is overbought, but we don't own any. Nothing to do.")
                
                if last_rsi < self.RSI_OVERSOLD:
                    if in_position:
                        print("It is oversold, but you already own it, nothing to do.")
                    else:
                        print("Oversold! Buy! Buy! Buy!")
                        # put binance buy order logic here
                        order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                        if order_succeeded:
                            in_position = True


def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

Strategy1 = RSI_Strategy(14,70,30)

def on_message(ws, message):
    global closes, in_position
    
    # print('received message')
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes: {closes}".format(closes = closes))

    Strategy1.run()
                
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()