#!pip install yfinance
import yfinance as yf

# Please use tickers that work on Yahoo Finance
cryptos = ["BTC-USD", "ADA-USD", "LTC-USD", "LINK-USD", "BNB-USD", "VET-USD"]


crypto1 = yf.download("BTC-USD", period="max")
crypto1 = crypto1[['Close', 'Open', 'High', 'Low']]
crypto1.index = crypto1.index.strftime('%d/%m/%Y')
crypto1.index.names = ['Timestamp']
crypto1 = crypto1.rename(columns={'Close': 'Closing Price (USD)', 'Open': '24h Open (USD)', 'High' : '24h High (USD)', 'Low' : '24h Low (USD)'})
crypto1.to_csv("BTC-USD" + ".csv", sep='\t')
