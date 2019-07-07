from pandas_datareader import data as pdr

import yfinance as yf
yf.pdr_override()


def fetch_to_file(name):
    name = str(name).upper()
    file_name = name + ".csv"
    try:
        data = pdr.get_data_yahoo(name)
        data.to_csv(file_name, encoding='utf-8')
    except ValueError as e:
        print(e)
        file_name == "null"

    return file_name
