import numpy as np
import pandas_datareader as pdr
import datetime as dt
import pandas as pd
import statsmodels.api as sm

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

#-----------------implementation 2 of CAPM -----------------
'''
Download monthly prices of Facebook and S&P 500 index from 2014 to 2017
CSV file downloaded from Yahoo File
start period: 02/11/2014 
end period: 30/11/2014
period format: DD/MM/YEAR
'''
fb = pd.read_csv('FB.csv', parse_dates=True, index_col='Date',)
sp_500 = pd.read_csv('^GSPC.csv', parse_dates=True, index_col='Date')

# joining the closing prices of the two datasets
monthly_prices = pd.concat([fb['Close'], sp_500['Close']], axis=1)
monthly_prices.columns = ['FB', '^GSPC']

# check the head of the dataframe
print(monthly_prices.head())

# calculate monthly returns
monthly_returns = monthly_prices.pct_change(1)
clean_monthly_returns = monthly_returns.dropna(axis=0)  # drop first missing row
print(clean_monthly_returns.head())

# split dependent and independent variable
X = clean_monthly_returns['^GSPC']
y = clean_monthly_returns['FB']

# Add a constant to the independent value
X1 = sm.add_constant(X)

# make regression model
model = sm.OLS(y, X1)

# fit model and print results
results = model.fit()
print(results.summary())
