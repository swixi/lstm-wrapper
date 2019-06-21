import numpy as np

from keras import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import History

import sklearn.metrics

import visual
import tools
import defaults


class KerasModel(object):
    """
    A class that is a container for a Keras Sequential() model.
    """
    def __init__(self, df, window_size, col_name):
        self.window_size = window_size
        self.df = df
        self.col_name = col_name
        self.stored_loss = []

        model = Sequential()
        model.add(LSTM(defaults.neurons, activation='relu', input_shape=(window_size, 1)))  # return_sequences=True,
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        self.model = model
        self.history = History()

        self.train_in, self.train_out, self.test_in, self.test_out = self.training_testing_data(defaults.test_ratio)

    # get a list of inputs (windows) and outputs (integers)
    # ratio is percentage of data that is test data
    # one featured (at the moment)
    def training_testing_data(self, test_data_ratio):
        # TODO: seems like bad methodology, change
        df = self.df
        col_name = self.col_name
        window_size = self.window_size

        test_data_index = int((1 - test_data_ratio) * len(df['Date']))
        # divider_date = df['Date'][test_data_index]

        train_df = df[:test_data_index]
        test_df = df[test_data_index:]

        train_col = train_df[col_name]
        test_col = test_df[col_name]

        # normalize
        # temp['Volume'] = temp['Volume']/temp['Volume'].iloc[0]

        # split each dataframe into overlapping chunks
        train_in = np.array([np.array(train_col[i:i + window_size]) for i in range(0, len(train_col) - window_size, 1)])
        test_in = np.array([np.array(test_col[i:i + window_size]) for i in range(0, len(test_col) - window_size, 1)])

        train_in = train_in.reshape(train_in.shape[0], train_in.shape[1], 1)
        test_in = test_in.reshape(test_in.shape[0], test_in.shape[1], 1)

        # output data
        train_out = np.array(train_col[window_size:])
        test_out = np.array(test_col[window_size:])

        return train_in, train_out, test_in, test_out

    # TODO: pop is broken?
    def add_layers(self, layers):
        if layers is None:
            return
        else:
            self.model.layers.pop()
            for _ in range(layers):
                self.model.add(LSTM(defaults.neurons, return_sequences=True, activation='relu'))
            self.model.add(Dense(1))
            self.model.compile(optimizer='adam', loss='mse')
            self.model.summary()

    def fit_model(self, epochs=defaults.epochs):
        # for i,j in zip(train_windows, train_out):
        #  print(i,j)

        self.model.fit(self.train_in, self.train_out, epochs=epochs, verbose=1)

    # trains the model until the percent change between losses is as small as desired,
    #   when averaged over $steps number of steps
    def fit_model_until_good(self, percent, steps=5):
        stored_loss = []
        while True:
            history = self.model.fit(self.train_in, self.train_out, epochs=1, verbose=1)
            stored_loss.extend(history.history['loss'])
            if len(stored_loss) >= steps:
                avg_percent_change = tools.average_percent_change(stored_loss)
                print(f"Moving percent change over {steps} steps: ", avg_percent_change)
                if avg_percent_change <= percent:
                    print(f"\nTotal epochs: {len(stored_loss)}")
                    break
        self.stored_loss = stored_loss

    def model_summary(self):
        self.model.summary()

    # call after fit_model
    def predict_on_test_data(self):
        return self.model.predict(self.test_in)

    def mse_on_test_data(self):
        predictions = self.predict_on_test_data()
        return sklearn.metrics.mean_squared_error(self.test_out, predictions)

    def plot_testing_vs_prediction(self, **indices):
        prediction = self.predict_on_test_data()
        visual.show_data_compare(self.df['Date'], prediction, self.test_out, 'Prediction', 'Actual (Test)', **indices)

    # predict an output based on a single window input
    # INPUT must be of length window_size
    def predict(self, test_datum):
        try:
            test_datum = np.array(test_datum).reshape(1, self.window_size, 1)
        except ValueError:
            print("Wrong shape?")
            return None

        return self.model.predict(test_datum, verbose=1)
