import os
import numpy as np

import pandas as pd

import stock_fetcher

FORMAT_ERROR = "Wrong format!"


# try to parse an int from a string
def try_parse_int(val):
    try:
        return int(val)
    except ValueError:
        return None


# INPUT: a list of strings where each string is known to represent an integer
# OUTPUT: the same list, now as integers
def parse_int_list(str_list):
    int_list = []
    for var in str_list:
        int_list.append(try_parse_int(var))

    return int_list


# INPUT: string of the form index1:index2
# OUTPUT: index1, index2 if in the correct form
#         None, None if in the the wrong form (with format error thrown)
# NOTE: None is allowed as an index if, e.g., there is a failed integer parse
# TODO: allow input as index1:index2 OR date1:date2
def parse_range(val):
    if val:
        vals = val[0].split(":")
        if len(vals) == 2:
            return try_parse_int(vals[0]), try_parse_int(vals[1])

    #print(FORMAT_ERROR)
    return None, None


def parse_data(data_file):
    df = pd.read_csv(data_file, sep=',')

    if 'Date' not in list(df):
        print("Need a \'Date\' column!")
        quit()

    # get file name without extension
    file_name = os.path.splitext(data_file)[0]
    file_name = os.path.basename(file_name)

    df['Name'] = file_name
    # label, _, _ = spy.split(sep='.')
    # label = os.path.basename(label)

    # df['Stock'] = label

    # extract Day from Date, shorten to 3 letters
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day'] = df['Date'].dt.day_name()
    df['Day'] = df['Day'].apply(lambda day: day[:3])

    print(file_name, "loaded")
    return df


# INPUT: a dataframe $df with a 'Day' column
# OUTPUT: a dictionary that has the average of $col_name for each day of $df
def avg_by_day(df, col_name):
    if col_name not in df:
        print("No such column")
        return

    averages = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}

    for key in averages:
        df_day = df[df['Day'] == key]
        if len(df_day):
            averages[key] = df_day[col_name].mean()

    return averages


# INPUT: a list of (positive) numbers
# OUTPUT: the average of the pairwise percent changes between successive numbers
def average_percent_change(nums):
    # pairwise percent changes
    changes = [(abs(nums[i+1]-nums[i]) / nums[i]) for i in range(0, len(nums)-1, 1)]
    return np.mean(changes)


def valid_csv(path):
    if os.path.isfile(path) and path.split(".")[1] == "csv":
        return True
    return False


def find_path():
    """ Find a path for csv if no path was specified
        Will only return after a valid path has been determined
        Can fetch a stock using yfinance and download a csv for the valid path (saved locally)
    """
    path = ""
    while not valid_csv(path):
        user_input = input("Enter path or call \'fetch TICKER\': ")
        if 'fetch' in user_input and len(user_input.split()) == 2:
            ticker = user_input.split()[1]
            file_name = stock_fetcher.fetch_to_file(ticker)
            path = os.path.join(os.getcwd(), file_name)
            print(path)
        else:
            path = user_input

    return path
