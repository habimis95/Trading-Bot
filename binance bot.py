{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "de0566fe-555e-4e74-a07f-c47e300ad992",
   "metadata": {},
   "outputs": [
    {
     "ename": "FileNotFoundError",
     "evalue": "[WinError 3] The system cannot find the path specified: '/home/habi_mis_95/csvs'",
     "output_type": "error",
     "traceback": [
      "\u001B[1;31m---------------------------------------------------------------------------\u001B[0m",
      "\u001B[1;31mFileNotFoundError\u001B[0m                         Traceback (most recent call last)",
      "\u001B[1;32m~\\AppData\\Local\\Temp/ipykernel_1548/2018830878.py\u001B[0m in \u001B[0;36m<module>\u001B[1;34m\u001B[0m\n\u001B[0;32m      7\u001B[0m \u001B[1;32mimport\u001B[0m \u001B[0mdatetime\u001B[0m \u001B[1;32mas\u001B[0m \u001B[0mdt\u001B[0m\u001B[1;33m\u001B[0m\u001B[1;33m\u001B[0m\u001B[0m\n\u001B[0;32m      8\u001B[0m \u001B[0mclient\u001B[0m \u001B[1;33m=\u001B[0m \u001B[0mClient\u001B[0m\u001B[1;33m(\u001B[0m\u001B[0mAPI_KEY\u001B[0m\u001B[1;33m,\u001B[0m \u001B[0mAPI_SECRET\u001B[0m\u001B[1;33m)\u001B[0m\u001B[1;33m\u001B[0m\u001B[1;33m\u001B[0m\u001B[0m\n\u001B[1;32m----> 9\u001B[1;33m \u001B[0msymbols\u001B[0m \u001B[1;33m=\u001B[0m \u001B[0mos\u001B[0m\u001B[1;33m.\u001B[0m\u001B[0mlistdir\u001B[0m\u001B[1;33m(\u001B[0m\u001B[1;34m'/home/habi_mis_95/csvs'\u001B[0m\u001B[1;33m)\u001B[0m\u001B[1;33m\u001B[0m\u001B[1;33m\u001B[0m\u001B[0m\n\u001B[0m",
      "\u001B[1;31mFileNotFoundError\u001B[0m: [WinError 3] The system cannot find the path specified: '/home/habi_mis_95/csvs'"
     ]
    }
   ],
   "source": [
    "from binance import Client\n",
    "import os\n",
    "from creds import API_KEY, API_SECRET\n",
    "import websocket\n",
    "import json\n",
    "import pandas as pd\n",
    "import datetime as dt\n",
    "client = Client(API_KEY, API_SECRET)\n",
    "symbols = os.listdir('/home/habi_mis_95/csvs')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "1ae0aea5-c88d-43b1-8860-a243b825469f",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "def last_n_min(symbol, lookback: int):\n",
    "    data = pd.read_csv('/home/habi_mis_95/csvs'+symbol, names = ['E', 'c'])\n",
    "    data['E'] = pd.to_datetime(data['E'])\n",
    "    before = pd.to_datetime('now') - dt.timedelta(minutes=lookback)\n",
    "    data = data[data.E >= before]\n",
    "    return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "outputs": [],
   "source": [
    "rets = []\n",
    "for symbol in symbols:\n",
    "    prices = last_n_min(symbol, 30)\n",
    "    cumret = (prices.c.pct_change() + 1).prod() - 1\n",
    "    rets.append(cumret)\n",
    "top_coin = symbols[rets.index(max(rets))]"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "outputs": [],
   "source": [
    "exclude = ['UP', 'DOWN', 'BEAR', 'BULL']"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "outputs": [],
   "source": [
    "non_lev = [symbol for symbol in symbols if all(excludes not in symbol for excludes in exclue )]"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7103310b-650c-4c3d-bebd-4fd9f4dc93cd",
   "metadata": {},
   "outputs": [],
   "source": [
    "inv_amt = 100\n",
    "info = client.get_symbol_info(symbol=top_coin)\n",
    "Lotsize = float([i for i in info['filters'] if i['filterType'] == 'LOT_SIZE'][0]['minQty'])\n",
    "prize = float(client.get_symbol_ticker(symbol=top_coin)['price'])\n",
    "buy_quantity = round(inv_amt/prize/Lotsize)*Lotsize\n",
    "\n",
    "if float([i for i in client.get_account()['balances'] if i['asset']=='USDT'][0]['free']) > 100:\n",
    "    print('enough funds, order will be executed')\n",
    "    order = client.order_limit_buy(symbol=top_coin, quantity=buy_quantity, price = prize)\n",
    "    print(order)\n",
    "else:\n",
    "    print('order has not been executed due to already invested')\n",
    "    quit()\n",
    "buyprice = float(order['price'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'top_coin' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001B[1;31m---------------------------------------------------------------------------\u001B[0m",
      "\u001B[1;31mNameError\u001B[0m                                 Traceback (most recent call last)",
      "\u001B[1;32m~\\AppData\\Local\\Temp/ipykernel_11396/942647809.py\u001B[0m in \u001B[0;36m<module>\u001B[1;34m\u001B[0m\n\u001B[1;32m----> 1\u001B[1;33m \u001B[0mstream\u001B[0m \u001B[1;33m=\u001B[0m \u001B[1;34mf\"wss://stream.binance.com:9443/ws/{top_coin.lower()}@trade\"\u001B[0m\u001B[1;33m\u001B[0m\u001B[1;33m\u001B[0m\u001B[0m\n\u001B[0m\u001B[0;32m      2\u001B[0m \u001B[1;32mdef\u001B[0m \u001B[0mon_message\u001B[0m\u001B[1;33m(\u001B[0m\u001B[0mws\u001B[0m\u001B[1;33m,\u001B[0m \u001B[0mmessage\u001B[0m\u001B[1;33m)\u001B[0m\u001B[1;33m:\u001B[0m\u001B[1;33m\u001B[0m\u001B[1;33m\u001B[0m\u001B[0m\n\u001B[0;32m      3\u001B[0m     \u001B[0mmsg\u001B[0m \u001B[1;33m=\u001B[0m \u001B[0mjson\u001B[0m\u001B[1;33m.\u001B[0m\u001B[0mloads\u001B[0m\u001B[1;33m(\u001B[0m\u001B[0mmessage\u001B[0m\u001B[1;33m)\u001B[0m\u001B[1;33m\u001B[0m\u001B[1;33m\u001B[0m\u001B[0m\n\u001B[0;32m      4\u001B[0m     \u001B[1;32mif\u001B[0m \u001B[0mfloat\u001B[0m\u001B[1;33m(\u001B[0m\u001B[0mmsg\u001B[0m\u001B[1;33m[\u001B[0m\u001B[1;34m'p'\u001B[0m\u001B[1;33m]\u001B[0m\u001B[1;33m)\u001B[0m \u001B[1;33m<\u001B[0m \u001B[0mbuyprice\u001B[0m \u001B[1;33m*\u001B[0m \u001B[1;36m0.97\u001B[0m \u001B[1;32mor\u001B[0m \u001B[0mfloat\u001B[0m\u001B[1;33m(\u001B[0m\u001B[0mmsg\u001B[0m\u001B[1;33m[\u001B[0m\u001B[1;34m'p'\u001B[0m\u001B[1;33m]\u001B[0m\u001B[1;33m)\u001B[0m \u001B[1;33m>\u001B[0m \u001B[1;36m1.05\u001B[0m \u001B[1;33m*\u001B[0m \u001B[0mbuyprice\u001B[0m\u001B[1;33m:\u001B[0m\u001B[1;33m\u001B[0m\u001B[1;33m\u001B[0m\u001B[0m\n\u001B[0;32m      5\u001B[0m         order = client.create_order(symbol=top_coin,\n",
      "\u001B[1;31mNameError\u001B[0m: name 'top_coin' is not defined"
     ]
    }
   ],
   "source": [
    "stream = f\"wss://stream.binance.com:9443/ws/{top_coin.lower()}@trade\"\n",
    "def on_message(ws, message):\n",
    "    msg = json.loads(message)\n",
    "    if float(msg['p']) < buyprice * 0.97 or float(msg['p']) > 1.05 * buyprice:\n",
    "        order = client.create_order(symbol=top_coin,\n",
    "                                    side='SELL',\n",
    "                                    type='MARKET',\n",
    "                                    quantity=buy_quantity)\n",
    "        print(order)\n",
    "        ws.close()\n",
    "ws = websocket.WebSocketApp(stream, on_message=on_message)\n",
    "ws.run_forever()"
   ],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "outputs": [],
   "source": [],
   "metadata": {
    "collapsed": false,
    "pycharm": {
     "name": "#%%\n"
    }
   }
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}