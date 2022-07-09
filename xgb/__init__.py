import xgboost as xgb
import numpy as np

from my_binance.k_line import KLine

class MyXgb:
    """
    Specify to train and predict the price using KLine
    """
    def __init__(self) -> None:
        """
        Initialize the MyXgb class
        """
        self._xgb_model = xgb.XGBRegressor(objective='reg:squarederror')

    """
    Train the model

    :param k_lines: List of KLines
    :return: None
    """
    def train(self, k_lines: list) -> None:
        # gets the features and labels from the k_lines
        features, labels = self._get_features_and_labels(k_lines)
        
        # train the model
        self._xgb_model.fit(features, labels)

    def predict(self, k_lines: list) -> list:
        """
        Predict the price

        :param k_lines: List of KLine
        :return: List of KLine
        """
        features, _ = self._get_features_and_labels(k_lines)
        predictions = self._xgb_model.predict(features)
        
        # prints the predictions as list
        for i in range(len(predictions)):
            print(f"{predictions[i]},", end=" ")

        return k_lines

    def _get_features_and_labels(self, k_lines: list):
        """
        Get the features and labels

        :param k_lines: List of KLine
        :return: features, labels
        """
        features = [
            [k_line.open, k_line.volume, k_line.n_trades] for k_line in k_lines
        ]
        labels = [k_line.close for k_line in k_lines]

        return features, labels

