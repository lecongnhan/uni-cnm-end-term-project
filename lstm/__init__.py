# https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/

import logging
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

tf.random.set_seed(7)

class MyLstm:
    def train(self, symbol_name: str, k_lines: list) -> None:
        logging.info(f"MyLstm is training {symbol_name}...")
        dataset = self._get_dataset(k_lines)
        logging.debug(f"dataset: {dataset} type: {type(dataset)}")

        # normalize the dataset
        # scaler = MinMaxScaler(feature_range=(0, 1))
        # dataset = scaler.fit_transform(dataset)
        logging.debug(f"dataset: {dataset} type: {type(dataset)}")

        # split into train and test sets
        train_size = int(len(dataset) * 0.9)
        test_size = len(dataset) - train_size
        train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
        print(len(train), len(test))

        # reshape into X=t and Y=t+1
        look_back = 1
        trainX, trainY = self._create_dataset(train, look_back)
        testX, testY = self._create_dataset(test, look_back)

        # reshape input to be [samples, time steps, features]
        logging.debug("shapoe:" + str(trainX.shape))
        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        # create and fit the LSTM network
        model = Sequential()
        model.add(LSTM(4, input_shape=(1, look_back)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)

        model.save(f'./models/lstm_{symbol_name}')

    def predict(self, symbol_name: str, k_lines: list) -> list:
        """
        Predict the next KLine
        :param symbol_name: Symbol name
        :param k_lines: List of KLine
        :return: List of KLine
        """
        logging.info(f"MyLstm is predicting {symbol_name}...")
        dataset = self._get_dataset(k_lines)
        # scaler = MinMaxScaler(feature_range=(0, 1))
        # dataset = scaler.fit_transform(dataset)

        # loads the model from disk
        model = self.load_model(symbol_name)

        # predicts
        dataset = self._get_dataset(k_lines)
        dataset = np.array(dataset)
        dataset = dataset.reshape(-1, 1, 1)
        predictions = model.predict(dataset)
        # predictions = scaler.inverse_transform(predictions)
        print(predictions)

        return predictions

    def _create_dataset(self, dataset, look_back=1):
        """
        convert an array of values into a dataset matrix
        """
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return np.array(dataX), np.array(dataY)

    def _get_dataset(self, k_lines: list) -> list:
        """
        Get the dataset
        :param k_lines: List of KLine
        :return: dataset
        """
        # convert to a numpy n dimenstional array        
        return np.array([[k_line.close] for k_line in k_lines])

    def load_model(self, symbol_name: str) -> None:
        """
        Load the model
        :param symbol_name: Symbol name
        :return: None
        """
        logging.info(f"MyLstm is loading {symbol_name}...")
        try:
            model = tf.keras.models.load_model(f'./models/lstm_{symbol_name}')
            return model
        except:
            return None