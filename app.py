from flask import Flask
import requests
from datetime import datetime, timedelta
from functools import wraps
from flask import  jsonify, request

import jwt
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"


BITTREX_API_BASE_URL = "https://api.bittrex.com/v3"

@auth.route("/generate_token")
def generate_token():
    exp_time = datetime.utcnow() + timedelta(seconds=1800)
    token = jwt.encode({"user": "test"},app.config["SECRET_KEY"],algorithm="HS256",)
    return jsonify({"token": token.decode("utf-8"), "expire": exp_time})

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]
        if not token:
            return jsonify({"Alert!": "Token is missing!"})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = data["user"]

        except:
            return jsonify({"Message": "Invalid token"})
        return func(*args, **kwargs)

    return decorated

@app.route("/market/summaries")
def get_market_summaries():
    
        response = requests.get(f"{BITTREX_API_BASE_URL}/markets/summaries")
        return jsonify(response.json())
   
@app.route("/markets/summary")
def get_market_summary():
    market_symbol = request.args.get("market")
    response = requests.get(f"{BITTREX_API_BASE_URL}/markets/{market_symbol}/summary")
    return jsonify(response.json())
if __name__ == '__main__':
    app.run(debug=True)