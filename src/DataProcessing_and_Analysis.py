# Simon Hugot
import os

from Event_detection import detect_event
from Daily_returns import daily_return_index
from CAAR import car
from CAPM import capm
from Ttest import one_sample_t_test, two_sample_t_test

# Main script
"""
# ------------ DAX ------------
# get list of stock for which changes were made in their security ratings#
# detect_event('rating_dax.csv', 'DAX')


# download the daily prices for the market and the stocks of the previous list.
daily_return_index("Data/DAX/StockChanges-DAX-Moody's.csv")
print("Daily return completed")

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
"""
# One sample T Test
one_sample_t_test("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30/Abnormal_returns.csv")
print("One sample T test completed")

# Two sample T Test
two_sample_t_test("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30/Abnormal_returns.csv")
print("Two sample T test completed")


"""
# ------------ FTSE ------------
# get list of stock for which changes were made in their security ratings#
# detect_event('rating_ftse.csv', '^FTSE')

# download the daily prices for the market and the stocks of the previous list.
daily_return_index("Data/^FTSE/StockChanges-^FTSE-Moody's.csv")

# compute the CAPM and extract alpha and beta values
for directory in os.listdir('Data/^FTSE/Prices'):
    path = "Data/^FTSE/Prices/" + directory
    capm(path)

# compute the CAAR
for filepath in os.listdir("Data/^FTSE/Prices"):
    path = "Data/^FTSE/Prices/" + filepath
    car(path)

# One sample T Test
one_sample_t_test("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30/Abnormal_returns.csv")

# Two sample T Test
two_sample_t_test("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30/Abnormal_returns.csv")

# ------------ NIKKEI ------------
# get list of stock for which changes were made in their security ratings#
# detect_event('rating_nikkei.csv', '^N225')

# download the daily prices for the market and the stocks of the previous list.
daily_return_index("Data/^N225/StockChanges-^N225-Moody's.csv")

# compute the CAPM and extract alpha and beta values
for directory in os.listdir('Data/^N225/Prices'):
    path = "Data/^N225/Prices/" + directory
    capm(path)

# compute the CAAR
for filepath in os.listdir("Data/^N225/Prices"):
    path = "Data/^N225/Prices/" + filepath
    car(path)

# One sample T Test
one_sample_t_test("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30/Abnormal_returns.csv")

# Two sample T Test
two_sample_t_test("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30/Abnormal_returns.csv")
"""
