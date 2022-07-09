import base64
import logging
from io import BytesIO
import time
from flask import Flask, make_response
from matplotlib.figure import Figure

app = Flask(__name__)

my_xgb = None
my_binance = None

@app.route("/")
def index():
    if not my_xgb:
        return "my_xgb is not set"
    if not my_binance:
        return "my_binance is not set"

    # get cur unix time
    now = int(round(time.time()))

    k_lines = my_binance.get_k_lines('HNTUSDT', limit=1000, from_time=now - 1000 * 60)
    predicted = my_xgb.predict("HNTUSDT", k_lines)

    # draw grapth with k_lines and predicted
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()

    # turns k_lines and predicted into a list of float and plot it
    float_arr = [k_line.close for k_line in k_lines]
    ax.plot(float_arr, label="k_lines")

    # plot predicted after k_lines
    ax.plot(predicted, label="predicted")
    # logging.info(f"predicted: {predicted}")


    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

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