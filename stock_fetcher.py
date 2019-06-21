from pandas_datareader import data as pdr

import yfinance as yf
yf.pdr_override()

data = pdr.get_data_yahoo("TRX")
data.to_csv("trx.csv", encoding='utf-8')
print(len(data))
print(data.head())
