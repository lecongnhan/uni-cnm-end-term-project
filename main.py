"""
The main program starts here.
"""
import os


from dotenv import load_dotenv
from binance import MyBinance

KEY_BINANCE_API_KEY = 'BINANCE_API_KEY'
KEY_BINANCE_API_SECRET = 'BINANCE_API_SECRET'


def main():
    """
    Main function
    """
    api_key = os.getenv(KEY_BINANCE_API_KEY)
    api_secret = os.getenv(KEY_BINANCE_API_SECRET)
    binance = MyBinance(api_key, api_secret)

    print(binance)

if __name__ == '__main__':
    load_dotenv()
    main()
