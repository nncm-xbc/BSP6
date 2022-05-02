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


def detect_event(raw_data, market):
    """
    Function that takes as input a raw csv file containing the event-log of security ratings
    for both the S&P and Moody's rating agencies.
    This function can only handle S&P and Moody's ratings as the grading scales are hardcoded.
    :param raw_data: csv file containing the event-log of the security ratings for S&P and Moody's on a specified market
    :param market: name of the market for which the security ratings are defined.
    :return: returns a csv that only contains the stocks for which the security ratings has been updated.
    The date of the change is specified, as well as whether it has been upgraded of downgraded.
    """

    doc = read_csv(raw_data)
    r, c = doc.shape
    changesList = []
    final_list = []

    rating_SP = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-", "CCC+", "CCC", "CCC-", "CC", "C", "D"]
    rating_moodys = ["Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2", "Baa3", "Ba1", "Ba2", "Ba3", "B1", "B2", "B3", "Caa1", "Caa2", "Caa3", "Caa"]

    names_agencies = {"S&P", "Moody's"}
    names_dates = {"DateS", "DateM"}

    # perform the actions for both security agencies
    for index_agency in range(len(names_agencies)):
        # example process for S&P
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
        # print(variation_list)
        final_list = []

        for tupl in variation_list:
            for tups in variation_list:
                if tupl[0] == tups[0] and tupl[1] != tups[1] and variation_list.index(tupl) < variation_list.index(tups):
                    # some ratings have a 'range' with either '/' or '-' as a seperator
                    # we will only take into account the lowest rating of the range
                    if ' / ' in tupl[2] or ' / ' in tups[2]:
                        st1 = tupl[2].split(' / ')[0]
                        st2 = tups[2].split(' / ')[0]
                        val_recent = rating_SP.index(st1)
                        val_old = rating_SP.index(st2)
                    elif ' - ' in tupl[2] or ' - ' in tups[2]:
                        st1 = tupl[2].split(' - ')[0]
                        st2 = tups[2].split(' - ')[0]
                        val_recent = rating_SP.index(st1)
                        val_old = rating_SP.index(st2)
                    else:
                        val_recent = rating_SP.index(tupl[2])
                        val_old = rating_SP.index(tups[2])

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
        '''
        for i in list(dict.fromkeys(final_list)):
            print(i)
        '''
        # create corresponding dataframe and save it as csv file in the folde corresponding to the correct market.
        df = pd.DataFrame(final_list, columns=["Stock", "Date", "Variation"])
        df.insert(0, "Rating Agency", names_agencies[index_agency])
        df.insert(0, "Market", market)

        # save the dataframe as a csv in the folder of its corresponding 
        df.to_csv(f'Data/{market}/StockChanges-{market}-{names_agencies[index_agency]}.csv', index=False)


        # daily index of the company and the market
        print(final_list)

def daily_returns(change_log):
    """
    Function that given a csv file containing stocks of a market and a date, computes the daily returns of both the stock
    and the market for a period of 1 year. This operation is computed for 3 different period: The first one is the year
    before the given date. The second period is the year containing the given date as its middle. The third period is
    the year after the given date.
    :param change_log: file containing the market name, stocks and their corresponding dates.
    :return: returns a collection of csv files that containg the daily prices of a stock on a market for a period of 1 year
    """

    for tuples in final_list:
        # Company growth index
        name = tuples[0]
        start_date = tuples[1].split("-")[0] + "-01-01"
        end_date = tuples[1].split("-")[0] + "-12-31"
        yearly_company_return = 0
        daily_returns = []

        prices_data = yf.download(name, start=start_date, end=end_date, interval="1d")
        prices_data = prices_data.drop(['High', 'Low', 'Adj Close', 'Volume', 'Open'], axis=1)

        r, c = prices_data.shape
        for row in range(r):
            prev_daily_return = prices_data.iloc[row - 1, 0]
            if prev_daily_return != 0:
                temp_daily_return = ((prices_data.iloc[row, 0] - prev_daily_return) / prev_daily_return) * 100
            else:
                temp_daily_return = 0
            daily_returns.append(temp_daily_return)
            yearly_company_return += temp_daily_return

        prices_data.insert(1, 'Daily return', daily_returns)

        # Market growth index
        market_data = yf.download('dax', start=start_date, end=end_date, interval="1d")
        market_data = market_data.drop(['High', 'Low', 'Adj Close', 'Volume', 'Open'], axis=1)
        yearly_market_return = 0
        daily_market_returns = []

        r, c = market_data.shape
        for row in range(r):
            prev_daily_market_return = market_data.iloc[row - 1, 0]
            if prev_daily_market_return != 0:
                temp_daily_return = ((market_data.iloc[row, 0] - prev_daily_market_return) / prev_daily_market_return) * 100
            else:
                temp_daily_return = 0
            daily_market_returns.append(temp_daily_return)
            yearly_market_return += temp_daily_return

        diff_sizes = prices_data.shape[0] - len(daily_market_returns)
        if diff_sizes > 0:
            prices_data.drop(index=prices_data.index[:diff_sizes], axis=0, inplace=True)
            prices_data.insert(2, 'Daily Market return', daily_market_returns)
            prices_data = prices_data.drop(['Close'], axis=1)
        else:
            daily_market_returns = daily_market_returns[: diff_sizes]
            prices_data.insert(2, 'Daily Market return', daily_market_returns)
            prices_data = prices_data.drop(['Close'], axis=1)
        # print(prices_data)

    # Function 3 that computes the CAPM of a given Stock and market in a time range.
    # return as CSV with Market, Stock, Alpha, Beta
    # Linear regression between market index and company index for a range of years

def capm():
    list_alpha = []
    list_beta = []

    '''
    prices_data.plot(x='Daily return', y='Daily Market return', style='o')
    plt.title('Market growth vs Company growth')
    plt.xlabel('Company growth')
    plt.ylabel('Market growth')
    plt.show()
    '''
    X = prices_data.iloc[:, :-1].values
    y = prices_data.iloc[:, 1].values

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

def abnormal_results():
