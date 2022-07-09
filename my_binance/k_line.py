"""
Contains class KLine
"""

class KLine:
    """
    A wrapper to represent a KLine
    """

    def __init__(self,
        open_time_: int,
        open_: float,
        high_: float,
        low_: float,
        close_: float,
        volume_: float,
        close_time_: int,
        quote_asset_volume_: str,
        n_trades_: int,
        taker_buy_base_asset: str,
        taker_buy_quote_asset_volume_: str,
        ignore: str
        ) -> None:
        """
        Initialize the KLine class

        :param open_time_: Open time
        :param open_: Open price
        :param high_: High price
        :param low_: Low price
        :param close_: Close price
        :param volume_: Volume
        :param close_time_: Close time
        :param quote_asset_volume_: Quote asset volume
        :param n_trades_: Number of trades
        :param taker_buy_base_asset: Taker buy base asset
        :param taker_buy_quote_asset_volume_: Taker buy quote asset volume
        :param ignore: Ignore
        """
        # https://python-binance.readthedocs.io/en/latest/binance.html#binance.client.Client.get_historical_klines
        # Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume,
        # Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore

        self._open_time = open_time_
        self._open = open_
        self._high = high_
        self._low = low_
        self._close = close_
        self._volume = volume_
        self._close_time = close_time_
        self._quote_asset_volume = quote_asset_volume_
        self._n_trades = n_trades_
        self._taker_buy_base_asset = taker_buy_base_asset
        self._taker_buy_quote_asset_volume = taker_buy_quote_asset_volume_
        self._ignore = ignore
    
    def __str__(self):
        return f"{self._open_time} {self._open} {self._high} {self._low} {self._close} {self._volume} {self._close_time}"

    @staticmethod
    def from_list(list_):
        """
        Creates a KLine object from a list of values
        :param list_: list of values
        :return: KLine object
        """
        return KLine(
            int(list_[0]), 
            float(list_[1]), 
            float(list_[2]),
            float(list_[3]), 
            float(list_[4]), 
            float(list_[5]), 
            int(list_[6]),
            list_[7], 
            int(list_[8]), 
            list_[9], 
            list_[10], 
            list_[11]
        )

    @property
    def close(self):
        return self._close

    @property
    def open(self):
        return self._open

    @property
    def volume(self):
        return self._volume

    @property
    def n_trades(self):
        return self._n_trades
