"""
The main program starts here.
"""
import os
import logging
import datetime
import asyncio

from dotenv import load_dotenv
from my_binance import MyBinance

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

    api_key = os.getenv(KEY_BINANCE_API_KEY)
    api_secret = os.getenv(KEY_BINANCE_API_SECRET)
    binance = MyBinance(api_key, api_secret)
    
    # print(binance.get_k_lines('HNTUSDT'))

    # subscribes to the symbols
    await binance.subcribe_symbol("HNTUSDT")
    await binance.subcribe_symbol("ZILTRY")

    await binance.update()
    
    # TODO: predict the price

if __name__ == '__main__':
    load_dotenv()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
