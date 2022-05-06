# Simon Hugot
import os
from pandas import *

def caar(filepath):
    alphabetavalues = read_csv(filepath + '/Alpha-Beta-Values.csv')

    filename_part = filepath.split('/')
    counter = 0

    final_values = []

    for filename in os.listdir(filepath):
        if filename_part[3][:9] in filename:
            doc = read_csv(filepath + '/' + filename)
            abv = 0

            # daily returns
            stock_return = doc['Stock return']
            market_return = doc['Market return']

            # a and b values for a year
            beta = alphabetavalues['Beta'][counter]
            alpha = alphabetavalues['Alpha'][counter]
            counter += 1

            # number of observations (days)
            N = 365
            for i in range(1, N+1):
                abv += (stock_return - beta * market_return - alpha)

            abv = abv/N
            final_values.append(abv)
        else:
            continue

    print(final_values)
