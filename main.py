"""
The main program starts here.
"""
import os
import logging
import datetime
import asyncio
import time

from dotenv import load_dotenv
from my_binance import MyBinance, SYMBOLS
from xgb import MyXgb
from app import app, set_my_binance, set_my_xgb

KEY_BINANCE_API_KEY = 'BINANCE_API_KEY'
KEY_BINANCE_API_SECRET = 'BINANCE_API_SECRET'


async def main():
    """
    Main function
    """

    # setups logging to a file named logs/[date]_[time].log and to the console
    now = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
    # creates log file if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging.basicConfig(
        filename=f'logs/{now}.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # makes logging output to the console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    # k_lines = binance.get_k_lines('HNTUSDT')
    # print([k_line.close for k_line in k_lines])
    # xgb = MyXgb()
    # xgb.train(k_lines[:900])
    # k_lines = xgb.predict(k_lines[900:950])
    # # print(k_lines)

    # subscribes to the symbols
    # await binance.subcribe_symbol("HNTUSDT")

    # TODO: predict the price

    api_key = os.getenv(KEY_BINANCE_API_KEY)
    api_secret = os.getenv(KEY_BINANCE_API_SECRET)
    my_binance = MyBinance(api_key, api_secret)

    my_xgb = MyXgb()

    # train first 10 symbols in SYMBOLS
    for symbol in SYMBOLS[:20]:
        # checks if the model exists
        xgb_model = my_xgb._load_model(symbol)
        if xgb_model is None:
            i = 1
            # get now in unix time
            now = int(round(time.time()))
            k_lines = my_binance.get_k_lines(symbol, limit=1000, from_time=now - (43 - i + 1) * 60 * 1000)
            my_xgb.train(symbol, k_lines)
            logging.info(f"Trained {symbol}")

    set_my_xgb(my_xgb)
    set_my_binance(my_binance)
    app.run()


if __name__ == '__main__':
    load_dotenv()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
