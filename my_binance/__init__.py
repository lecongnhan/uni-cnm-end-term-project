"""
Initial file for binance handler
Go to https://www.binance.com/en/my/settings/api-management for API Keys managements
Binance constants: binance.client.Client
"""

import asyncio
import logging

from binance.client import Client
from binance.streams import BinanceSocketManager
from my_binance.k_line import KLine
from .symbols import SYMBOLS

def handle_socket_message(msg):
    print("ackj")
    print(f"message type: {msg['e']}")
    print(msg)

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
        self._websockets = []

    def get_k_lines(self, symbol, interval:str=Client.KLINE_INTERVAL_1MINUTE, limit=1000):
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

        res = self._client.get_historical_klines(symbol, interval,'1 day ago UTC', limit=limit)
        logging.debug('got %d K Lines for %s', len(res), symbol)
        logging.debug(res)

        return list(map(KLine.from_list, res))

    async def subcribe_symbol(self, symbol:str):
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
        self._websockets.append(ws)
    
    async def update(self):
        while True:
            # listens for all websockets in self._websockets
            msgs = await asyncio.gather(*[ws.recv() for ws in self._websockets])
            for msg in msgs:
                handle_socket_message(msg)
                
            await asyncio.sleep(1)


