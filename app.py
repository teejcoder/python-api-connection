from flask import Flask, request, jsonify
import flask
import requests

app = Flask(__name__)

@app.route('/')
def hello_flask():
    return flask.render_template("hello.html")

@app.route('/dashboard')
def dashboard():
    return flask.render_template("dashboard.html")

@app.route('/get-market-data')
def get_market_data():
    response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=QLYRUT52O4STJNRG')
    data = response.json()
    last_10_days = list(data['Time Series (Daily)'].keys())[:10]
    filtered_data = {day: data['Time Series (Daily)'][day] for day in last_10_days}
    return jsonify(filtered_data)


if __name__ == '__main__':
    app.run(debug=True)
