"""
Initial file for binance handler
Go to https://www.binance.com/en/my/settings/api-management for API Keys managements
Binance constants: binance.client.Client
"""


from binance.client import Client

from my_binance.k_line import KLine


class MyBinance:
    """
    A wrapper to Binance Websocket (ThreadedWebsocketManager) that andles all actions from/to
    Binance
    """
    def __init__(self, api_key:str=None, api_secret:str=None):
        """
        Initialize the Binance class

        :param api_key: Binance API Key
        :param api_secret: Binance API Secret
        """
        self._api_key = api_key
        self._api_secret = api_secret

        # inits the websocket manager
        self._client = Client(self._api_key, self._api_secret)

        # gets data of the last 100 candles
        for data in self._client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1MINUTE,'1 hour ago UTC'):
            k_line = KLine.from_list(data)
            print(k_line)


    def _handle_socket_message(self, msg):
        print(f"message type: {msg['e']}")
        print(msg)
