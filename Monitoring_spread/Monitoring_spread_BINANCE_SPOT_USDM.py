# -*- coding: utf-8 -*-
import ccxt
import ccxt.pro
from asyncio import run, gather, sleep


orderbooks = {}
b_ask_binance = {}
b_ask_bybit = {}
b_ask_upbit = {}
bid_bybit = 0
ask_bybit = 0
bid_binance = 0
ask_binance = 0

def handle_all_orderbooks(orderbooks):
    # print('We have the following orderbooks:')
    global bid_bybit, ask_bybit, bid_binance, ask_binance
    
    for exchange_id, orderbooks_by_symbol in orderbooks.items():
        for symbol in orderbooks_by_symbol.keys():
            orderbook = orderbooks_by_symbol[symbol]
            # print(ccxt.pro.Exchange.iso8601(orderbook['timestamp']), exchange_id, symbol, orderbook['asks'][0], orderbook['bids'][0])
            if exchange_id == 'binance':
                ask_binance = orderbook['asks'][0][0]
                bid_binance = orderbook['bids'][0][0]
            elif exchange_id == 'binanceusdm':
                ask_bybit = orderbook['asks'][0][0]
                bid_bybit = orderbook['bids'][0][0]

    if bid_bybit != 0 and ask_bybit != 0 and bid_binance != 0 and ask_binance != 0:
        spread_1 = ask_bybit / bid_binance  # higher number. You can "buy"
        spread_2 = bid_bybit / ask_binance  # lower number. You can sell.
    else:
        spread_1 = 0
        spread_2 = 0
            # print(b_ask_binance)

    print('You can sell for: ', spread_2, 'You can buy for: ', spread_1, symbol, "ask binance: ", ask_binance, bid_binance, ask_bybit, bid_bybit)    


async def handling_loop(orderbooks):
    delay = 3
    while True:
        await sleep(delay)
        handle_all_orderbooks(orderbooks)


async def symbol_loop(exchange, symbol):
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol)
            # orderbook = await exchange.watch_ticker(symbol)
            orderbooks[exchange.id] = orderbooks.get(exchange.id, {})
            orderbooks[exchange.id][symbol] = orderbook
        except Exception as e:
            print(str(e))
            # raise e  # uncomment to break all loops in case of an error in any one of them
            break  # you can break just this one loop if it fails


async def exchange_loop(exchange_id, symbols):

    if exchange_id == 'binanceusdm':
        # exchange = ccxt.pro.binance({'options': {'defaultType': 'future'}})
        exchange = ccxt.pro.binanceusdm()
    elif exchange_id == 'binance':
        exchange = ccxt.pro.binance()
    # elif exchange_id == 'binance_spot':
    #     exchange = ccxt.pro.binance()
    # elif exchange_id == 'bybit':
    #     exchange = ccxt.pro.bybit()
    # markets = exchange.load_markets()
    # print(markets)
    loops = [symbol_loop(exchange, symbol) for symbol in symbols]
    await gather(*loops)
    await exchange.close()


async def main():
    # symbols_bybit = ['BNXUSDT']
    symbols_binance = ['ETH/USDT']
    # symbols_binance_spot = ['ICXUSDT']

    symbols_up = ['ETH/BUSD']
    exchanges = {
        # 'bybit': symbols_bybit,
        'binance': symbols_binance,
        # 'binance_spot': symbols_binance_spot
        'binanceusdm' : symbols_up
    }
    loops = [exchange_loop(exchange_id, symbols) for exchange_id, symbols in exchanges.items()]
    loops += [handling_loop(orderbooks)]
    await gather(*loops)


run(main())