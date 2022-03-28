#!pip install yfinance
import yfinance as yf

# Please use tickers that work on Yahoo Finance
cryptos = ["BTC-USD", "ADA-USD", "LTC-USD", "LINK-USD", "BNB-USD", "VET-USD"]

for crypto in cryptos:
    crypto1 = yf.download(crypto, period="max")
    crypto1.to_csv(str(crypto) + ".csv", sep='\t')
