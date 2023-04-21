import requests
from flask import Blueprint, jsonify, request

from .auth import token_required


bitrix = Blueprint("bitrix", __name__, url_prefix="/api/v1/")


BITTREX_API_BASE_URL = "https://api.bittrex.com/v3"



@bitrix.route("/market/summaries", methods=["GET"])
@token_required
def get_market_summaries():
    try:
        response = requests.get(f"{BITTREX_API_BASE_URL}/markets/summaries")
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as err:
        return jsonify({"error": str(err)}), 500


@bitrix.route("/markets/summary", methods=["GET"])
@token_required
def get_market_summary():
    market_symbol = request.args.get("market")
    if not market_symbol:
        return jsonify({"error": "Market symbol not provided."}), 400
    response = requests.get(f"{BITTREX_API_BASE_URL}/markets/{market_symbol}/summary")
    return jsonify(response.json()), 200
