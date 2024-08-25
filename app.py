from flask import Flask, request, jsonify
import flask
import requests
import pandas as pd
import logging
from flask_caching import Cache
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA

# Configure cache
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)
cache.init_app(app)

@app.route('/')
def hello_flask():
    return flask.render_template("hello.html")

@app.route('/dashboard')
def dashboard():
    return flask.render_template("dashboard.html")

def fetch_data():
    # Fetch stock prices
    response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=8MD9CMGZZZWUWWPY')
    data = response.json()
    stock_prices = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
    stock_prices.index = pd.to_datetime(stock_prices.index)
    stock_prices = stock_prices.astype(float)

    # Fetch additional data (dummy data for illustration)
    # You would replace these with actual API calls or data sources
    # technical_indicators = pd.DataFrame({
    #     'date': stock_prices.index,
    #     'sma': stock_prices['4. close'].rolling(window=20).mean(),
    #     'ema': stock_prices['4. close'].ewm(span=20, adjust=False).mean(),
    #     'rsi': 100 - (100 / (1 + stock_prices['4. close'].pct_change().rolling(window=14).mean())),
    #     'macd': stock_prices['4. close'].ewm(span=12, adjust=False).mean() - stock_prices['4. close'].ewm(span=26, adjust=False).mean()
    # }).set_index('date')

    # fundamental_data = pd.DataFrame({
    #     'date': stock_prices.index,
    #     'pe_ratio': 25,  # Dummy data
    #     'dividend_yield': 1.5  # Dummy data
    # }).set_index('date')

    # market_sentiment = pd.DataFrame({
    #     'date': stock_prices.index,
    #     'sentiment': 0.5  # Dummy data
    # }).set_index('date')

    # economic_indicators = pd.DataFrame({
    #     'date': stock_prices.index,
    #     'interest_rate': 0.05,  # Dummy data
    #     'inflation_rate': 0.02  # Dummy data
    # }).set_index('date')

    # external_factors = pd.DataFrame({
    #     'date': stock_prices.index,
    #     'geopolitical_event': 0  # Dummy data
    # }).set_index('date')

    # Combine all data into a single DataFrame
    combined_data = stock_prices
    # combined_data = stock_prices.join([technical_indicators, fundamental_data, market_sentiment, economic_indicators, external_factors])
    # combined_data.fillna(method='ffill', inplace=True)

    return combined_data

@app.route('/get-market-data')
@cache.cached(timeout=500)
def get_market_data():
    #Fetches the last 30 days of market data and returns it as JSON.
    logger.info("Fetching market data")
    combined_data = fetch_data()
    last_30_days = combined_data.head(30)
    logger.info("Market data fetched and cached")
    return last_30_days.to_json(orient='index')

@app.route('/predict', methods=['GET'])
@cache.cached(timeout=500)
def predict():
    ##Uses ARIMA model to predict the closing stock price and returns the prediction as JSON.
    logger.info("Fetching prediction data")
    combined_data = fetch_data()
    model = ARIMA(combined_data['4. close'], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=1)
    logger.info("Prediction data fetched and cached")
    return jsonify({'predicted_close': forecast[0]})

@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    ##Clears the cache.
    cache.clear()
    return jsonify({'message': 'Cache cleared'})

if __name__ == '__main__':
    app.run(debug=True)