#!/usr/bin/env python
# coding: utf-8

import os
import argparse

# internal imports
import data_tools
import visual
from data_tools import parse_data
import keras_wrapper
from keras_wrapper import KerasModel


def main():
    # parse args from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path')
    parser.add_argument('-c', '--col_name')
    parser.add_argument('--stock')
    args = parser.parse_args()

    if not args.path:
        print("No path specified")
        quit()

    if not args.col_name:
        print("No column specified")
        quit()

    data_file = args.path
    col_name = args.col_name

    if not os.path.isfile(data_file):
        print(data_file, "is not a file!")
        quit()

    if args.stock:
        is_stock = True

    df = parse_data(data_file)

    user_loop(df, col_name)


def user_loop(df, col_name):
    while True:
        user_input = input("Enter a command: ")
        user_input = user_input.split()
        keyword = user_input[0]

        if 'help' in user_input:
            print("Commands: help, define $col_name, plot, avg, lstm, quit")
        elif keyword == 'define':
            col_name = user_input[1]
        elif keyword == 'plot':
            visual.show_data(df, col_name)
        elif keyword == 'avg':
            print(data_tools.avg_by_day(df, col_name) if col_name in df else "No such column")
        elif keyword == 'lstm':
            window_size = int(input("Window size? "))
            model = KerasModel(df, window_size, col_name)
            model.fit_model()
            model.plot_training_vs_testing()
        elif 'quit' in user_input:
            quit()


"""


test_datum = np.array(test_in[0]).reshape(1, window_size, 1)

print(model.predict(test_datum, verbose=0))




mae = sklearn.metrics.mean_absolute_error(test_out, predictions)

print('MAE: {}'.format(mae))
"""


if __name__ == "__main__":
    main()
