# Simon Hugot
import os
import pandas as pd
from pandas import *
import yfinance as yf
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta


def daily_return_index(filepath):
    """
    Function that given a csv file containing stocks of a market and a date, computes the daily returns of both the stock
    and the market for a period of 1 year. This operation is computed for 3 different period: The first one is the year
    before the given date. The second period is the year containing the given date as its middle. The third period is
    the year after the given date.
    :param filepath: path of the file containing the market name, stocks and their corresponding dates.
    :return: returns a collection of csv files that containg the daily prices of a stock on a market for a period of 1 year
    """
    doc = read_csv(filepath)

    for index, row in doc.iterrows():
        # Company growth index
        stock_name = row['Stock']
        market_name = row['Market']
        agency_name = row['Rating Agency']
        date = row['Date']

        # compute the three 1 year periods
        dtObj = datetime.strptime(date, '%Y-%m-%d')
        start_dates = [ dtObj - relativedelta(years=1), dtObj - relativedelta(months=6), dtObj]
        end_dates = [dtObj, dtObj + relativedelta(months=6), dtObj + relativedelta(years=1)]

        # compute the whole thing for every period (here x3)
        for iter in range(len(start_dates)):
            yearly_company_return = 0
            daily_returns = []

            # download raw daily prices for the given period
            stock_prices = yf.download(stock_name, start=start_dates[iter], end=end_dates[iter], interval="1d")
            market_prices = yf.download(market_name, start=start_dates[iter], end=end_dates[iter], interval="1d")

            # we only need the closing prices to compute the daily returns and then the growth indexes
            stock_prices = stock_prices.drop(['High', 'Low', 'Adj Close', 'Volume', 'Open'], axis=1)
            market_prices = market_prices.drop(['High', 'Low', 'Adj Close', 'Volume', 'Open'], axis=1)
            prices_list = [stock_prices, market_prices]

            final_indexes = pd.DataFrame(index=stock_prices.index)

            # Compute the daily returns for the stock values
            for i in range(len(prices_list)):
                daily_price = 0
                for index, row in prices_list[i].iterrows():
                    prev_daily_price = daily_price
                    daily_price = row['Close']
                    if prev_daily_price != 0:
                        daily_return = ((daily_price - prev_daily_price) / prev_daily_price) * 100
                    else:
                        daily_return = 0
                    daily_returns.append(daily_return)

                if i == 0:
                    final_indexes.insert(i, 'Stock return', daily_returns)
                elif i == 1:
                    final_indexes.insert(i, 'Market return', daily_return)

            # save the dataframe as a csv in the correct folder
            start_datestr = start_dates[iter].strftime('%Y-%m-%d')
            end_datestr = end_dates[iter].strftime('%Y-%m-%d')
            end_datestr0 = end_dates[0].strftime('%Y-%m-%d')
            print(end_datestr0)
            temp_path = 'Data/' + market_name + '/Prices/' + stock_name + '-' + agency_name + '-' + end_datestr0
            if os.path.isdir(temp_path):
                filepath = Path(temp_path + '/' + stock_name + '-' + agency_name + '-' + start_datestr + '-' + end_datestr + '.csv')
                final_indexes.to_csv(filepath)
            else:
                os.makedirs(temp_path)
                filepath = Path(temp_path + '/' + stock_name + '-' + agency_name + '-' + start_datestr + '-' + end_datestr + '.csv')
                final_indexes.to_csv(filepath)
