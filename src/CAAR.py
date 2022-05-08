# Simon Hugot
import os
import pandas as pd
from pandas import *


def car(filepath):
    alphabetavalues = read_csv(filepath + '/Alpha-Beta-Values.csv')
    filepath_part = filepath.split('/')
    counter = 0

    final_values = []
    final_df = pd.DataFrame()

    for filename in os.listdir(filepath):
        if filepath_part[3][:9] in filename:
            doc = read_csv(filepath + '/' + filename)

            # daily returns
            stock_return = doc['Stock return']
            market_return = doc['Market return']

            # a and b values for a year
            beta = alphabetavalues['Beta'][counter]
            alpha = alphabetavalues['Alpha'][counter]

            # computation of the abnormal returns for every day in the 3 one year periods.
            abv = (stock_return - beta * market_return - alpha)
            abv = abv.tolist()

            final_values.append(abv)

            col_name = filename.split('.')[1][22:]
            final_df[col_name] = pd.Series(final_values[counter])
            final_df.to_csv(filepath + '/Abnormal_returns.csv')
            counter += 1
        else:
            continue
