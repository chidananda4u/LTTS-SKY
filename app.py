from flask import Flask
import requests

app = Flask(__name__)

BITTREX_API_BASE_URL = "https://api.bittrex.com/v3"

# @app.route('/')
# def get_market_summaries():
    
#         response = requests.get(f"{BITTREX_API_BASE_URL}/markets/summaries")
#         return jsonify(response.json())
   
@app.route('/')
def get_market_summary():
    market_symbol = request.args.get("market")
    response = requests.get(f"{BITTREX_API_BASE_URL}/markets/{market_symbol}/summary")
    return jsonify(response.json())
if __name__ == '__main__':
    app.run(debug=True)