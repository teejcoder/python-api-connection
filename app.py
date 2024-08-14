from flask import Flask, request, jsonify
import flask
from flask import Flask, request, jsonify
import flask
import requests

app = Flask(__name__)

app = Flask(__name__)

@app.route('/')
def hello_flask():
    return flask.render_template("hello.html")

@app.route('/get-market-data')
def get_market_data():
    response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=QLYRUT52O4STJNRG')
    return jsonify(response.json())
    

@app.route('/get-user/<user_id>')
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "johndoe@mail.com"
    }
    
    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
    return jsonify(user_data), 200



if __name__ == '__main__':
    app.run(debug=True)
