import functools


# INPUT: a dataframe $df with a 'Day' column
# OUTPUT: a dictionary that has the average of $col_name for each day of $df
# TODO: check, if the df has no Sat column, does this still work?
import os

import pandas as pd


def avg_by_day(df, col_name):
    if col_name not in df:
        print("No such column")
        return

    averages = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}

    for key in averages:
        df_day = df[df['Day'] == key]
        if len(df_day):
            averages[key] = functools.reduce(lambda x, y: x + y, df_day[col_name], 0) / len(df_day)
    return averages


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