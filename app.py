from flask import Flask, request, jsonify
import flask
import requests
import pandas as pd
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA

# app.py

app = Flask(__name__)

@app.route('/')
def hello_flask():
    """
    Renders the hello.html template when the root URL is accessed.
    """
    return flask.render_template("hello.html")

@app.route('/dashboard')
def dashboard():
    """
    Renders the dashboard.html template when the /dashboard URL is accessed.
    """
    return flask.render_template("dashboard.html")

def fetch_data():
    """
    Fetches stock prices and additional data from APIs or data sources.
    Returns a combined DataFrame of the fetched data.
    """
    # Fetch stock prices
    response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=J1TVNBS1XD48RGXL')
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
def get_market_data():
    """
    Fetches the last 30 days of market data and returns it as JSON.
    """
    combined_data = fetch_data()
    last_30_days = combined_data.head(30)
    return last_30_days.to_json(orient='index')

@app.route('/predict', methods=['GET'])
def predict():
    """
    Uses ARIMA model to predict the closing stock price and returns the prediction as JSON.
    """
    combined_data = fetch_data()
    model = ARIMA(combined_data['4. close'], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=1)
    return jsonify({'predicted_close': forecast[0]})

if __name__ == '__main__':
    app.run(debug=True)