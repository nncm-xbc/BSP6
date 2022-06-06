# Simon Hugot
import os
import pandas as pd
from Event_detection import detect_event
from Daily_returns import daily_return_index
from CAAR import car
from CAPM import capm
from Ttest import one_sample_t_test, two_sample_t_test
import os
from pandas import *

# Main script

# ------------ DAX ------------
# get list of stock for which changes were made in their security ratings#
# detect_event('rating_dax.csv', 'DAX')

"""
# download the daily prices for the market and the stocks of the previous list.
daily_return_index("Data/DAX/StockChanges-DAX-Moody's.csv")
print("Daily return completed")

# remove empty csvs for which data does not exist.
for directory in os.listdir('Data/Dax/Prices'):
    path = 'Data/Dax/Prices/' + directory
    for filename in os.listdir(path):
        path2 = path + '/' + filename
        print(path2)
        df = pd.read_csv(path2)
        if df.empty:
            os.remove(path2)

# compute the CAPM and extract alpha and beta values
for directory in os.listdir('Data/DAX/Prices'):
    path = "Data/DAX/Prices/" + directory
    capm(path)
print("CAPM completed")

# compute the CAAR
for filepath in os.listdir("Data/DAX/Prices"):
    path = "Data/DAX/Prices/" + filepath
    car(path)
print("CAR completed")

# One sample T Test
for directory in os.listdir("C:/Users/Leshu/PycharmProjects/BSP6/Data/DAX/Prices"):
    path = "C:/Users/Leshu/PycharmProjects/BSP6/Data/DAX/Prices/" + directory
    one_sample_t_test(path)
print("One sample T test completed")

# Two sample T Test
two_sample_t_test("C:/Users/Leshu/PycharmProjects/BSP6/Data/DAX/Prices")
"""
two_sample_results = read_csv("C:/Users/Leshu/PycharmProjects/BSP6/Data/DAX/Two_sample_results.csv")
StockChanges = read_csv("C:/Users/Leshu/PycharmProjects/BSP6/Data/DAX/StockChanges-DAX-Moody's.csv")

variation_list = []
for i in range(len(two_sample_results)):
    NameList = two_sample_results.iloc[i].tolist()[1].split('-')
    for j in range(len(StockChanges)):
        if NameList[1] == StockChanges.iloc[j].tolist()[2] and NameList[0] == StockChanges.iloc[j].tolist()[3] and str(NameList[2])+'-'+str(NameList[3])+'-'+str(NameList[4]) == StockChanges.iloc[j].tolist()[4]:
            variation_list.append(StockChanges.iloc[j].tolist()[5])
            print(two_sample_results.iloc[i].tolist()[1])
            print(StockChanges.iloc[j].tolist()[5])
        else:
            continue

two_sample_results['Variations'] = variation_list
two_sample_results.to_csv("C:/Users/Leshu/PycharmProjects/BSP6/Data/DAX/Two_sample_results.csv")
"""
# ------------ FTSE ------------
# get list of stock for which changes were made in their security ratings#
# detect_event('rating_ftse.csv', '^FTSE')

# download the daily prices for the market and the stocks of the previous list.
daily_return_index("Data/^FTSE/StockChanges-^FTSE-Moody's.csv")

# remove empty csvs for which data does not exist.
for directory in os.listdir('Data/^FTSE/Prices'):
    path = 'Data/^FTSE/Prices/' + directory
    for filename in os.listdir(path):
        path2 = path + '/' + filename
        print(path2)
        df = pd.read_csv(path2)
        if df.empty:
            os.remove(path2)

# compute the CAPM and extract alpha and beta values
for directory in os.listdir('Data/^FTSE/Prices'):
    path = "Data/^FTSE/Prices/" + directory
    capm(path)

# compute the CAAR
for filepath in os.listdir("C:/Users/Leshu/PycharmProjects/BSP6/Data/^FTSE/Prices"):
    path = "C:/Users/Leshu/PycharmProjects/BSP6/Data/^FTSE/Prices/" + filepath
    car(path)

# One sample T Test
one_sample_t_test("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30/Abnormal_returns.csv")

# Two sample T Test
two_sample_t_test("C:/Users/Leshu/PycharmProjects/BSP6/Data/^FTSE/Prices")

# ------------ NIKKEI ------------
# get list of stock for which changes were made in their security ratings#
# detect_event('rating_nikkei.csv', '^N225')

# download the daily prices for the market and the stocks of the previous list.
daily_return_index("Data/^N225/StockChanges-^N225-Moody's.csv")

# remove empty csvs for which data does not exist.
for directory in os.listdir('Data/^N225/Prices'):
    path = 'Data/^N225/Prices/' + directory
    for filename in os.listdir(path):
        path2 = path + '/' + filename
        df = pd.read_csv(path2)
        if df.empty:
            os.remove(path2)

# compute the CAPM and extract alpha and beta values
for directory in os.listdir('Data/^N225/Prices'):
    path = "Data/^N225/Prices/" + directory
    capm(path)

# compute the CAAR
for filepath in os.listdir("C:/Users/Leshu/PycharmProjects/BSP6/Data/^N225/Prices"):
    path = "C:/Users/Leshu/PycharmProjects/BSP6/Data/^N225/Prices/" + filepath
    car(path)

# One sample T Test
one_sample_t_test("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30/Abnormal_returns.csv")

# Two sample T Test
two_sample_t_test("C:/Users/Leshu/PycharmProjects/BSP6/Data/^N225/Prices")
"""