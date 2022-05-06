# Simon Hugot
import os
import pandas as pd
from pandas import *
from pathlib import Path
from scipy import stats
import statsmodels.api as sm


def capm(filepath):
    """
    Function that computes the alpha and beta values for a stock in a given market over the course of a year.
    :param filepath: path to the file that contains the stock and market prices.
    :return: returns the alpha and beta values in a csv file
    """
    alpha_values = []
    beta_values = []

    for filename in os.listdir(filepath):

        doc = read_csv(filepath+'/'+filename)

        x = doc['Stock return'].iloc[1:]
        y = doc['Market return'].iloc[1:]

        # Add a constant to the independent value
        x1 = sm.add_constant(x)

        # make regression model
        model = sm.OLS(y, x1)

        # fit model and print results
        # results = model.fit()

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        # beta and alpha values
        alpha_values.append(intercept)
        beta_values.append(slope)

    analysis_val = pd.DataFrame(alpha_values, columns=['Alpha'])
    analysis_val['Beta'] = beta_values

    path = filepath.partition('/')
    path_complete = Path(path[0] + '/' + path[2] + '/Alpha-Beta-Values.csv')
    analysis_val.to_csv(path_complete)
