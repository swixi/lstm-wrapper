# lstm-wrapper
A command line user interface for running a Keras-based LSTM. Currently only parses csv.

Run `python main.py -p PATH -c COLUMN` from the command line, where PATH is the full path to a csv file and COLUMN is the name of the column in the csv that you wish to analyze. If no path is specified, one can be selected from the CLI, or stock data can be fetched to a csv file.

Type `help` to see the available commands. After running the lstm, you can type `help` again to see lstm-specific commands.

Initial configuration is specified in the **config** file.

## Dependencies
pandas

sklearn

numpy

tensorflow and keras

yfinance (can be avoided if path of csv is specified on command line)
