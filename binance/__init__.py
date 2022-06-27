"""
Initial file for binance handler
Go to https://www.binance.com/en/my/settings/api-management for API Keys managements
"""

class MyBinance:
    """
    A wrapper to Binance Websocket (ThreadedWebsocketManager) that andles all actions from/to
    Binance
    """
    def __init__(self, api_key=None, api_secret=None):
        """
        Initialize the Binance class

        :param api_key: API Key
        :param api_secret: API Secret
        """
        self._api_key = api_key
        self._api_secret = api_secret
