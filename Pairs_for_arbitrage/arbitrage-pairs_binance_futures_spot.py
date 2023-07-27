# -*- coding: utf-8 -*-

import os
import sys
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402


def style(s, style):
    return style + s + '\033[0m'


def green(s):
    return style(s, '\033[92m')


def blue(s):
    return style(s, '\033[94m')


def yellow(s):
    return style(s, '\033[93m')


def red(s):
    return style(s, '\033[91m')


def pink(s):
    return style(s, '\033[95m')


def bold(s):
    return style(s, '\033[1m')


def underline(s):
    return style(s, '\033[4m')


def dump(*args):
    print(' '.join([str(arg) for arg in args]))


def print_exchanges():
    dump('Supported exchanges:', ', '.join(ccxt.exchanges))


def print_usage():
    dump("Usage: python " + sys.argv[0], green('id1'), yellow('id2'), blue('id3'), '...')



ids = ['binance', 'binanceusdm']
exchanges = {}
dump(ids)
dump(yellow(' '.join(ids)))
for id in ids:  # load all markets from all exchange exchanges

    # instantiate the exchange by id
    exchange = getattr(ccxt, id)()

    # save it in a dictionary under its id for future use
    exchanges[id] = exchange

    # load all markets from the exchange
    markets = exchange.load_markets()


    dump(green(id), 'loaded', green(str(len(exchange.symbols))), 'markets')

dump(green('Loaded all markets'))

allSymbols = [symbol for id in ids for symbol in exchanges[id].symbols]

# get all unique symbols
uniqueSymbols = list(set(allSymbols))

# filter out symbols that are not present on at least two exchanges
arbitrableSymbols = sorted([symbol for symbol in uniqueSymbols if allSymbols.count(symbol) > 1])
# print a table of arbitrable symbols
print(arbitrableSymbols)
print(len(arbitrableSymbols))
table = []
dump(green(' symbol          | ' + ''.join([' {:<15} | '.format(id) for id in ids])))
dump(green(''.join(['-----------------+-' for x in range(0, len(ids) + 1)])))

for symbol in arbitrableSymbols:
    string = ' {:<15} | '.format(symbol)
    row = {}
    for id in ids:
        # if a symbol is present on a exchange print that exchange's id in the row
        string += ' {:<15} | '.format(id if symbol in exchanges[id].symbols else '')
    dump(string)
