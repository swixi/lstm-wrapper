#!/usr/bin/env python
# coding: utf-8

import os
import argparse

import data_tools
import visual
from data_tools import parse_data


def main():
    # parse args from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path')
    parser.add_argument('--stock')
    args = parser.parse_args()

    if not args.path:
        print("No path specified")
        quit()

    data_file = args.path

    if not os.path.isfile(data_file):
        print(data_file, "is not a file!")
        quit()

    if args.stock:
        is_stock = True

    df = parse_data(data_file)

    user_loop(df)


def user_loop(df):
    while True:
        user_input = input("Enter a command: ")
        user_input = user_input.split()

        if 'help' in user_input:
            print("Commands: help, plot $col_name, avg $col_name, quit")
        elif user_input[0] == 'plot':
            col_name = user_input[1]
            visual.show_data(df, col_name)
        elif user_input[0] == 'avg':
            col_name = user_input[1]
            print(data_tools.avg_by_day(df, col_name) if col_name in df else "No such column")
        elif 'quit' in user_input:
            quit()


"""
window_size = 5

model = init_lstm(window_size)

train_in, train_out, test_in, test_out = training_testing_data(window_size, 0.1, 'Volume')

# for i,j in zip(train_windows, train_out):
#  print(i,j)

model.fit(train_in, train_out, epochs=5, verbose=0)

test_datum = np.array(test_in[0]).reshape(1, window_size, 1)

print(model.predict(test_datum, verbose=0))

predictions = model.predict(test_in)

plt.plot(test_out, label='actual')
plt.plot(predictions, label='prediction')
plt.xlim([0, 100])
plt.legend()
plt.show()

mae = sklearn.metrics.mean_absolute_error(test_out, predictions)

print('MAE: {}'.format(mae))
"""


if __name__ == "__main__":
    main()
