# Simon Hugot
from Event_detection import detect_event
from Daily_returns import daily_return_index
from CAAR import car
from CAPM import capm

# Main script
# get list of stock for which changes were made in their security ratings
# detect_event('rating_dax.csv', 'DAX')

# download the daily prices for the market and the stocks of the previous list.
# daily_return_index("Data/DAX/StockChanges-DAX-Moody's.csv")

# compute the CAPM and extract alpha and beta values
# for directory in os.listdir('Data/DAX/Prices'):
#    print(directory)
#    capm("Data/DAX/Prices/" + directory)

# compute the CAAR
car("Data/DAX/Prices/1COV.DE-Moody's-2018-07-30")
