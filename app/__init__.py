import base64
import json
import logging
from io import BytesIO
import os
import time
from flask import Flask, make_response, render_template, request
from matplotlib.figure import Figure

app = Flask(__name__)

my_xgb = None
my_binance = None

@app.route("/")
def index():
    # reders the index.html file
    return render_template("index.html")

@app.route("/graph")
def graph():
    if not my_xgb:
        return "my_xgb is not set"
    if not my_binance:
        return "my_binance is not set"

    # get symbol from url
    symbol = request.args.get("symbol")
    if not symbol:
        return "symbol is not defined"
    
    # get method from url
    method = request.args.get("method")
    if not method:
        return "method is not defined"

    # get type from url
    type_ = request.args.get("type")
    if not type_:
        return "type is not defined"

    # get cur unix time
    now = int(round(time.time()))

    k_lines = my_binance.get_k_lines(symbol, limit=1000, from_time=now - 1000 * 60)

    predicted = []
    if (method == "xgboost"):
        predicted = my_xgb.predict(symbol, k_lines)

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

@app.route("/symbols")
def symbols():
    if not my_binance:
        return "my_binance is not set"

    # get all models saved in ./models
    symbols = [file_name.split("_")[1] for file_name in os.listdir("./models")]
    symbols = [file_name.split(".")[0] for file_name in symbols]
    return json.dumps(symbols)


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