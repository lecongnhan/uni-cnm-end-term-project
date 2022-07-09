from asyncio.log import logger
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
        self._xgb_model = None

    """
    Train the model

    :param k_lines: List of KLines
    :return: None
    """
    def train(self, symbol_name: str, k_lines: list) -> None:
        """
        Train the model
        
        :param k_lines: List of KLine
        :return: None
        """
        xgb_model = xgb.XGBRegressor(objective='reg:squarederror')

        # gets the features and labels from the k_lines
        features, labels = self._get_features_and_labels(k_lines)

        # checks if the features and labels are valid
        # features needs to be a 2 dimensional array
        # labels needs to be a 1 dimensional array
        if not features or len(features) == 0 or len(features[0]) != 3:
            logger.error(f"features are not valid: {features}")
            return None
        
        # train the model
        xgb_model.fit(features, labels)

        # save the model
        xgb_model.save_model(f'./models/xgb_{symbol_name}.model')

        return xgb_model


    def predict(self, symbol: str, k_lines: list) -> list:
        """
        Predict the price

        :param k_lines: List of KLine
        :return: List of KLine
        """
        xgb_model = self._load_model(symbol)

        features, _ = self._get_features_and_labels(k_lines)
        if not len(features):
            return []
            
        predictions = xgb_model.predict(xgb.DMatrix(features))
        
        # # prints the predictions as list
        # for i in range(len(predictions)):
        #     print(f"{predictions[i]},", end=" ")

        return predictions

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

        # converts features to DMatrix object
        if len(features) > 0:
            features = np.array(features)
            labels = np.array(labels)
            return features, labels

        return [], []

    def _load_model(self, symbol_name: str):
        """
        Load the model if exists

        :param symbol_name: Symbol name
        :return: None
        """
        try:
            xgb_model = xgb.Booster()
            xgb_model.load_model(f'models/xgb_{symbol_name}.model')
            return xgb_model
        except Exception as exception:
            logger.exception(f"load model for symbol {symbol_name}", exception)
            self._xgb_model = None
            return None

my_xgb = MyXgb()