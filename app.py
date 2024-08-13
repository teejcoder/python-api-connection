from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_flask():

    return "Hello, Flask!"

@app.route('/api')
def api_route():
    print(2 + 2)
    return "Hello, Flask! this is the /api route"

@app.route('/market-data')
def market_data(url,r):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'
    r = requests.get(url)
    data = r.json()
    return jsonify(data)


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

@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(debug=True)
