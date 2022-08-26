from binance import Client
import os
from creds import API_KEY, API_SECRET
import websocket
import json
import pandas as pd
import datetime as dt
client = Client(API_KEY, API_SECRET)
symbols = os.listdir('/home/habi_mis_95/csvs')
#%%
def last_n_min(symbol, lookback: int):
    data = pd.read_csv('/home/habi_mis_95/csvs'+symbol, names = ['E', 'c'])
    data['E'] = pd.to_datetime(data['E'])
    before = pd.to_datetime('now') - dt.timedelta(minutes=lookback)
    data = data[data.E >= before]
    return data
#%%
rets = []
for symbol in symbols:
    prices = last_n_min(symbol, 30)
    cumret = (prices.c.pct_change() + 1).prod() - 1
    rets.append(cumret)
top_coin = symbols[rets.index(max(rets))]
#%%
exclude = ['UP', 'DOWN', 'BEAR', 'BULL']
#%%
non_lev = [symbol for symbol in symbols if all(excludes not in symbol for excludes in exclue )]
#%%
inv_amt = 100
info = client.get_symbol_info(symbol=top_coin)
Lotsize = float([i for i in info['filters'] if i['filterType'] == 'LOT_SIZE'][0]['minQty'])
prize = float(client.get_symbol_ticker(symbol=top_coin)['price'])
buy_quantity = round(inv_amt/prize/Lotsize)*Lotsize

if float([i for i in client.get_account()['balances'] if i['asset']=='USDT'][0]['free']) > 100:
    print('enough funds, order will be executed')
    order = client.order_limit_buy(symbol=top_coin, quantity=buy_quantity, price = prize)
    print(order)
else:
    print('order has not been executed due to already invested')
    quit()
buyprice = float(order['price'])
#%%
stream = f"wss://stream.binance.com:9443/ws/{top_coin.lower()}@trade"
def on_message(ws, message):
    msg = json.loads(message)
    if float(msg['p']) < buyprice * 0.97 or float(msg['p']) > 1.05 * buyprice:
        order = client.create_order(symbol=top_coin,
                                    side='SELL',
                                    type='MARKET',
                                    quantity=buy_quantity)
        print(order)
        ws.close()
ws = websocket.WebSocketApp(stream, on_message=on_message)
ws.run_forever()
