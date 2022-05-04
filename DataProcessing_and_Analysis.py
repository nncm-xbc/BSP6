# Simon Hugot
import pandas as pd
from pandas import *
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import seaborn as sns
from iteration_utilities import flatten
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta


def detect_event(raw_data, market):
    """
    Function that takes as input a raw csv file containing the event-log of security ratings
    for both the S&P and Moody's rating agencies.
    This function can only handle S&P and Moody's ratings as the grading scales are hardcoded.
    :param raw_data: name of the csv file containing the event-log of the security ratings for S&P and Moody's on a specified market
    :param market: name of the market for which the security ratings are defined.
    :return: returns a csv that only contains the stocks for which the security ratings has been updated.
    The date of the change is specified, as well as whether it has been upgraded of downgraded.
    """

    doc = read_csv(raw_data)
    r, c = doc.shape

    # first S&P second Moody's
    rating_scales = [["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-", "CCC+", "CCC", "CCC-", "CC", "C", "D"],
                     ["Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2", "Baa3", "Ba1", "Ba2", "Ba3", "B1", "B2", "B3", "Caa1", "Caa2", "Caa3", "Caa"]]

    names_agencies = ["S&P", "Moody's"]
    names_dates = ["DateS", "DateM"]

    # perform the actions for both security agencies
    for index_agency in range(len(names_agencies)):
        variation_list = []
        for col in range(1, c):
            ratings_list = []
            dates_list = []
            prices_list = []

            # create 3 lists for each comopany: ratings, dates, prices (makes it easier to compare the indexes)
            for row in range(1, r):
                if names_agencies[index_agency] in doc.iloc[row, 0]:
                    ratings_list.append(doc.iloc[row, col])
                elif names_dates[index_agency] in doc.iloc[row, 0]:
                    dates_list.append(doc.iloc[row, col])
                else:
                    prices_list.append(doc.iloc[row, col])

            # check that the rating for that year (row) is different from ***(null)
            for i in ratings_list:
                if i != "***":
                    temp_index = ratings_list.index(i)
                    variation_list.append((doc.iloc[r - 1, col], dates_list[temp_index], i))

        final_list = []

        for tupl in variation_list:
            for tups in variation_list:
                if tupl[0] == tups[0] and tupl[1] != tups[1] and variation_list.index(tupl) < variation_list.index(tups):
                    # some ratings have a 'range' with either '/' or '-' as a seperator
                    # we will only take into account the lowest rating of the range
                    if ' / ' in tupl[2] or ' / ' in tups[2]:
                        st1 = tupl[2].split(' / ')[0]
                        st2 = tups[2].split(' / ')[0]
                        val_recent = rating_scales[index_agency].index(st1)
                        val_old = rating_scales[index_agency].index(st2)
                    elif ' - ' in tupl[2] or ' - ' in tups[2]:
                        st1 = tupl[2].split(' - ')[0]
                        st2 = tups[2].split(' - ')[0]
                        val_recent = rating_scales[index_agency].index(st1)
                        val_old = rating_scales[index_agency].index(st2)
                    else:
                        val_recent = rating_scales[index_agency].index(tupl[2])
                        val_old = rating_scales[index_agency].index(tups[2])

                    # check indexes and attribute the correct change to the corresponding difference
                    if val_recent < val_old:
                        final_list.append((tupl[0], tupl[1], "Increased"))
                    elif val_recent > val_old:
                        final_list.append((tupl[0], tupl[1], "Decreased"))
                    else:
                        # if the comparison cannot be made the change is simply non-available
                        # ie: first rating change of the dataset
                        final_list.append((tupl[0], tupl[1], "N/A"))
                elif tupl[0] == tups[0] and tupl[1] != tups[1] and variation_list.index(tupl) > variation_list.index(tups):
                    final_list.append((tupl[0], tupl[1], "N/A"))
                else:
                    continue

        # create corresponding dataframe and save it as csv file in the folde corresponding to the correct market.
        df = pd.DataFrame(final_list, columns=["Stock", "Date", "Variation"])
        df.insert(0, "Rating Agency", names_agencies[index_agency])
        df.insert(0, "Market", market)
        df.drop_duplicates(subset=None, keep="first", inplace=True)

        # save the dataframe as a csv in the correct folder
        filepath = Path('Data/'+market+'/StockChanges-'+market+'-'+names_agencies[index_agency]+'.csv')
        df.to_csv(filepath)


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
            filepath = Path('Data/' + market_name + '/Prices/' + stock_name + '-' + agency_name + '-' + start_datestr + '-' + end_datestr + '.csv')
            final_indexes.to_csv(filepath)


# Function 3 that computes the CAPM of a given Stock and market in a time range.
# return as CSV with Market, Stock, Alpha, Beta
# Linear regression between market index and company index for a range of years
def capm(filepath):
    doc = read_csv(filepath)

    list_alpha = []
    list_beta = []

    X = doc['Stock return'].values
    y = doc['Market return'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    # prediction
    y_pred = regressor.predict(X_test)
    df_prediction = DataFrame({'Actual': y_test, 'Predicted': y_pred})

    alpha = regressor.intercept_
    beta = regressor.coef_[0]

    list_alpha.append(alpha)
    list_beta.append(beta)

    size_diff = len(X) - len(y_pred)
    padding_list = []
    for i in range(size_diff):
        padding_list.append(None)
    y_pred = np.append(y_pred, np.asarray(padding_list))

    XYdf = pd.DataFrame()
    XYdf.insert(0, 'X', value=list(flatten(X)))
    XYdf.insert(1, 'Y', value=y_pred)

    '''
    sns.regplot(x='X', y='Y', data=XYdf)
    plt.title('Y_pred against X values')
    plt.show()
    '''

    ABdf = pd.DataFrame()
    ABdf.insert(0, 'Alpha', value=list_alpha)
    ABdf.insert(1, 'Beta', value=list_beta)

    sns.regplot(x="Alpha", y="Beta", data=ABdf)
    plt.title('Alpha against Beta values')
    plt.show()

    print("Alpha values: ", list_alpha, "\n Beta values: ", list_beta)

def CAAR(filepath):
    # sum-from1toN(stock_return - stock_beta * market_return - alpha)/N
    # whats N ?

    stock_return
    market_return


# Main
# get list of stock for which changes were made in their security ratings
# detect_event('rating_dax.csv', 'DAX')

# download the daily prices for the market and the stocks of the previous list.
# daily_return_index("Data/DAX/StockChanges-DAX-Moody's.csv")

# compute the CAPM and extract alpha and beta values
# example with one file
capm("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30/1COV.DE-Moody's-2017-07-30-2018-07-30.csv")
