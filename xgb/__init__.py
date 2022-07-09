from asyncio.log import logger
import os
from sklearn.metrics import mean_squared_error
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
        # gets the model if exists
        xgb_model = self._load_model(symbol_name)
        trained = True
        if xgb_model is None:
            xgb_model = xgb.XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
                                colsample_bynode=1, colsample_bytree=1, gamma=0,
                                importance_type='gain', learning_rate=0.1, max_delta_step=0,
                                max_depth=3, min_child_weight=1, missing=1, n_estimators=100,
                                n_jobs=1, nthread=None, objective='reg:squarederror', random_state=0,
                                reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
                                silent=None, subsample=1, verbosity=1)
            trained = False

        # gets the features and labels from the k_lines
        features, labels = self._get_features_and_labels(k_lines)

        # checks if the features and labels are valid
        # features needs to be a 2 dimensional array
        # labels needs to be a 1 dimensional array
        if features is None or len(features) == 0 or len(features[0]) != 3:
            logger.error(f"features are not valid: {features}")
            return None
        
        # train the model
        xgb_model.fit(features, labels, xgb_model=xgb_model if trained else None)

        # score = xgb_model.score(features, labels)
        # logger.info(f"score: {score}")

        # dump the model
        xgb_model.save_model(f'./models/xgb_{symbol_name}.model')
        # xgb_model.save_model(f'models/xgb_{symbol_name}.model')

        xgb_model.save_model(f'./models/xgb_{symbol_name}.model')


        return xgb_model


    def predict(self, symbol: str, k_lines: list) -> list:
        """
        Predict the price

        :param k_lines: List of KLine
        :return: List of KLine
        """
        xgb_model = self._load_model(symbol)
        if xgb_model is None:
            return []

        features, ytest = self._get_features_and_labels(k_lines)
        if not len(features) or features is None:
            logger.error("features are not valid: " + str(features))
            return []
            
        print(features)
        predictions = xgb_model.predict(features)

        # mse
        mse = mean_squared_error(ytest, predictions)
        # logger.info(f"test: {ytest}")
        logger.info(f"mse: {mse}")

        
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
        # checks if the model file exists
        if not os.path.isfile(f'./models/xgb_{symbol_name}.model'):
            return None

        try:
            xgb_model = xgb.XGBRegressor(objective='reg:squarederror')
            xgb_model.load_model(f'./models/xgb_{symbol_name}.model')
            # xgb_model.load_model(f'models/xgb_{symbol_name}.model')
            return xgb_model
        except Exception as exception:
            logger.exception("load model for symbol %s", symbol_name)
            logger.exception(exception)
            self._xgb_model = None
            return None

my_xgb = MyXgb()