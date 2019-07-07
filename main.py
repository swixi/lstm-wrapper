#!/usr/bin/env python
# coding: utf-8

import argparse

# internal imports
import tools
import defaults
import visual
from tools import parse_data, valid_csv, find_path
from keras_wrapper import KerasModel


def find_column():
    pass


def main():
    # parse args from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path')
    parser.add_argument('-c', '--col_name')
    parser.add_argument('--stock')
    args = parser.parse_args()

    if not args.path or not valid_csv(args.path):
        print("No path specified (or not a valid path)")
        args.path = find_path()

    if not args.col_name:
        print("No column specified!")
        find_column()

    data_file = args.path
    col_name = args.col_name

    if args.stock:
        is_stock = True

    df = parse_data(data_file)

    user_loop(df, col_name)


def user_loop(df, col_name):
    while True:
        user_input = input("Enter a command (column = {}): ".format(col_name))
        user_input = user_input.split()
        keyword = user_input[0]
        params = user_input[1:]

        if 'help' in user_input:
            print("Commands: help, column, column $col_name, plot [index1:index2], avg, lstm [window size], quit")
        elif keyword == 'column':
            if len(keyword.split()) == 1:
                print("Columns:\n", list(df))
            else:
                col_name = user_input[1]
        elif keyword == 'plot':
            index1, index2 = tools.parse_range(params)
            visual.show_data(df, col_name, index1=index1, index2=index2)
        elif keyword == 'avg':
            print(tools.avg_by_day(df, col_name) if col_name in df else "No such column")
        elif keyword == 'lstm':
            if params:
                window_size = tools.try_parse_int(params[0])
            else:
                window_size = defaults.window_size

            lstm_loop(df, col_name, window_size)
        elif 'quit' in user_input:
            quit()


def lstm_loop(df, col_name, window_size):
    model = KerasModel(df, window_size, col_name)
    print("Initiated LSTM with window size {}.".format(window_size), "\n")

    trained = False
    needs_training = ['plot', 'predict', 'summary', 'mse']

    while True:
        user_input = input("Enter an LSTM command ({}, {}): ".format(col_name, window_size)).split()
        keyword = user_input[0]
        params = user_input[1:]

        if 'help' in user_input:
            print("Commands: help, window $window_size, train [$epochs], train until $percent [$steps], "
                  "plot [index1:index2], layers, predict $tuple, summary")
            continue
        if keyword == "back":
            return
        if keyword in needs_training and not trained:
            print("Need to train model first.")
            continue

        # If a non-valid window size is entered (eg NaN, then keep the current one)
        if keyword == "window":
            if params:
                new_window_size = tools.try_parse_int(params[0])
                if new_window_size is not None:
                    window_size = new_window_size
                    model = KerasModel(df, window_size, col_name)
                    print("Initiated LSTM with window size {}.".format(window_size), "\n")
                    trained = False
        # train [$epochs]. If no epochs specified, defaults to $epochs defined in defaults.py.
        elif keyword == "train":
            epochs = defaults.epochs

            if params:
                # Run training until the loss has small variation (determined by $percent)
                # TODO: add $steps option
                if 'until' in params:
                    percent = float(params[1])
                    model.fit_model_until_good(percent)
                    trained = True
                    continue

                # If 'until' was not in params, proceed with normal training
                temp = tools.try_parse_int(params[0])
                if temp is not None:
                    epochs = temp

            model.fit_model(epochs=epochs)
            trained = True
        # TODO: fix
        elif keyword == "layers":
            if params:
                layers = tools.try_parse_int(params[0])
                model.add_layers(layers)
                print(f"Added {layers} layers.")
                trained = False
        elif keyword == "plot":
            index1, index2 = tools.parse_range(params)
            model.plot_testing_vs_prediction(index1=index1, index2=index2)
        # predict $vars
        # where $vars is a comma delimited sequence of $window_size many numbers (single-feature)
        # This is for user predictions, not test data
        elif keyword == "predict":
            print("Prediction: {}".format(model.predict(params[0].split(","))))
        elif keyword == "summary":
            model.model_summary()
        # Calculate mean squared error on the test data
        elif keyword == "mse":
            print(f"MSE on prediction vs test data: {model.mse_on_test_data()}")
        elif 'quit' in user_input:
            quit()


if __name__ == "__main__":
    main()
