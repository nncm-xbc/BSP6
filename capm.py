import datetime
import yfinance as yf
import pandas as pd
import statsmodels.api as sm
"""
import numpy as np
import pandas_datareader as pdr
import datetime as dt

#-----------------implementation 1 of CAPM -----------------

tickers = ['AAPL', 'MSFT', 'TWTR', 'IBM', '^GSPC']
start = dt.datetime(2015, 12, 1)
end = dt.datetime(2021, 1, 1)

data = pdr.get_data_yahoo(tickers, start, end, interval="m")

data = data['Adj Close']

log_returns = np.log(data / data.shift())

cov = log_returns.cov()
var = log_returns['^GSPC'].var()

beta = cov.loc['AAPL', '^GSPC'] / var

risk_free_return = 0.0138
market_return = .105
expected_return = risk_free_return + beta * (market_return - risk_free_return)
"""

#-----------------implementation 2 of CAPM -----------------

def capm(year, stock, market):
    #download daily prices of stock and market into csv
    min_year = year-1
    max_year = year+1
    start = datetime.datetime(min_year, 1, 1)
    end = datetime.datetime(max_year, 1, 1)

    mk = yf.download(market, start=start, end=end, interval="1d")
    st = yf.download(stock, start=start, end=end, interval="1d")

    # joining the closing prices of the two datasets
    # st = stock; mk = market
    daily_prices = pd.concat([st['Close'], mk['Close']], axis=1)
    daily_prices.columns = [stock, market]

    # check the head of the dataframe
    print(daily_prices.head())

    # calculate daily returns
    daily_returns = daily_prices.pct_change(1)
    clean_daily_returns = daily_returns.dropna(axis=0)  # drop first missing row
    print(clean_daily_returns.head())

    # split dependent and independent variable
    X = clean_daily_returns[market]
    y = clean_daily_returns[stock]

    # Add a constant to the independent value
    X1 = sm.add_constant(X)

    # make regression model
    model = sm.OLS(y, X1)

    # fit model and print results
    results = model.fit()
    print(results.summary())

st_name = "ADS.DE"
mk_name = "dax"
ch_year = 2021
capm(stock=st_name, market=mk_name, year=ch_year)
