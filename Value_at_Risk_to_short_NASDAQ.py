# calculate capital allocation for shorting  NASDAQ, using Value at Risk (VaR)

import numpy as np
    
# VaR
def VaR(returns, confidence_level):
    # sort returns
    returns = np.sort(returns)
    # calculate VaR
    var = returns[int(np.ceil(len(returns) * (1 - confidence_level))) - 1]
    return var

# get returns of NASDAQ using Yahoo finance, yf Python library

import yfinance as yf

nasdaq = yf.Ticker("NDX")

# get historical prices

hist = nasdaq.history(period="2y", interval="1d")

# get returns

returns = hist["Close"].pct_change()

# calculate VaR

var = VaR(returns, 0.05)

# print VaR

print("VaR: ", var)
