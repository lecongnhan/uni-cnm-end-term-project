"""
Initial file for binance handler
Go to https://www.binance.com/en/my/settings/api-management for API Keys managements
Binance constants: binance.client.Client
"""

import asyncio
import logging
import time

from binance.client import Client
from binance.streams import BinanceSocketManager
from my_binance.k_line import KLine
from .symbols import SYMBOLS


class _Ws_Subcribable:
    def __init__(self, ws, callback:callable=None):
        self._ws = ws
        self._callback = callback

    def callback(self, args):
        print(args)

        if self._callback:
            self._callback(args)

    @property
    def ws(self):
        return self._ws

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

        self._client = Client(self._api_key, self._api_secret)
        self._binance_socket_manager = BinanceSocketManager(self._client)

        """
        Dictionary of websockets
        Key: str
        Value: _WS_Subcribable
        """
        self._websockets = {}

    def get_k_lines(self, symbol, interval:str=Client.KLINE_INTERVAL_1MINUTE, limit=1000, from_time=None):
        """
        Get the K Lines for a symbol

        :param symbol: Symbol
        :param limit: Limit
        :return: List of KLine objects
        """
        logging.debug(
            'getting k lines for %s at interval %s with limit %d',
            symbol,
            interval,
            limit
        )
        if not symbol:
            raise ValueError('Symbol is required')

        if symbol not in SYMBOLS:
            raise ValueError(f'Symbol {symbol} is not supported')

        if not from_time:
            # get cur unix timestamp
            from_time = int(round(time.time())) - limit * 60

        res = self._client.get_historical_klines(symbol, interval, from_time * 1000, limit=limit)
        logging.debug('got %d K Lines for %s', len(res), symbol)
        logging.debug(res)

        return list(map(KLine.from_list, res))

    def handle_socket_message(self, msg):
        logging.debug("Received new message from socket: %s", msg)
        symbol = msg['s']

        if symbol in self._websockets:
            ws_subcriptable = self._websockets[symbol]
            ws_subcriptable.callback(msg)

    async def subcribe_symbol(self, symbol:str, callback:callable=None):
        """
        Subscribe to a symbol

        :param symbol: Symbol to subscribe
        """
        logging.debug('subscribing to %s', symbol)

        if not symbol:
            raise ValueError('Symbol is required')

        if symbol not in SYMBOLS:
            raise ValueError(f'Symbol {symbol} is not supported')

        ws = self._binance_socket_manager.kline_socket(symbol, Client.KLINE_INTERVAL_1MINUTE)
        await ws.connect()
        self._websockets[symbol] = _Ws_Subcribable(ws, callback)

    def unsubcribe_symbol(self, symbol:str):
        """
        Unsubscribe from a symbol
        Currently just remove its socket reference so it won't be listening anymore

        :param symbol: Symbol to unsubscribe
        """
        logging.debug('unsubscribing from %s', symbol)

        if not symbol:
            raise ValueError('Symbol is required')

        if symbol not in SYMBOLS:
            raise ValueError(f'Symbol {symbol} is not supported')

        if symbol in self._websockets:
            del self._websockets[symbol]
    
    async def update(self):
        """
        Listens to all the websockets
        """
        while True:
            # listens for all websockets in self._websockets
            msgs = await asyncio.gather(*[self._websockets[ws].ws.recv() for ws in self._websockets])
            for msg in msgs:
                self.handle_socket_message(msg)

            await asyncio.sleep(1)
