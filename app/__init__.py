from flask import Flask
app = Flask(__name__)

my_xgb = None
my_binance = None

@app.route("/")
def index():
    if not my_xgb:
        return "my_xgb is not set"
    if not my_binance:
        return "my_binance is not set"

    k_lines = my_binance.get_k_lines('AVAXBTC')
    predicted = my_xgb.predict("AVAXBTC", k_lines)
    return str(predicted)

@app.route("/graph")
def graph():
    return "Hello, World!"

def set_my_xgb(xgb_):
    """
    Sets the global variable my_xgb
    
    :param my_xgb: MyXgb
    :return: None
    """
    global my_xgb
    my_xgb = xgb_

def set_my_binance(binance_):
    """
    Sets the global variable my_binance
    
    :param my_binance: MyBinance
    :return: None
    """
    global my_binance
    my_binance = binance_