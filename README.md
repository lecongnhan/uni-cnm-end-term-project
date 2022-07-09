# uni-cnm-end-term-project
# features
Predicts close price from binance using `xgbooster`, `rnn`, or `lstm`

# Usage
1. Get a Binance API and add them to `.env` file (see `.env.example`)

2. Install dependencies
`pip install -r requirements.txt`

3. Run
`python main.py`

# models
If you want to re-train a model, remove its model file in ./models
If you want to support more model, change the number of model in `main.py line 65`: `for symbol in SYMBOLS[:5]:`, it will train and save the missing models.

