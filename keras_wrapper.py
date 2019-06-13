import numpy as np

from keras import Sequential
from keras.layers import LSTM, Dense


# get a list of inputs (windows) and outputs (integers)
# ratio is percentage of data that is test data
# one featured (at the moment)
def training_testing_data(window_size, test_data_ratio, col_name):
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


# LSTM with specified window_size
# allows ONE feature right now
def init_lstm(window_size):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(window_size, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    return model