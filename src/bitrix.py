import requests
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .auth import token_required
from .constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

bitrix = Blueprint("bitrix", __name__, url_prefix="/api/v1/")


BITTREX_API_BASE_URL = "https://api.bittrex.com/v3"



@bitrix.route("/market/summaries", methods=["GET"])
@token_required
@swag_from('./docs/bitrix/market_summaries.yml')
def get_market_summaries():
    try:
        response = requests.get(f"{BITTREX_API_BASE_URL}/markets/summaries")
        response.raise_for_status()
        return jsonify(response.json()), HTTP_200_OK
    except requests.exceptions.RequestException as err:
        return jsonify({"error": str(err)}), HTTP_500_INTERNAL_SERVER_ERROR


@bitrix.route("/markets/summary", methods=["GET"])
@token_required
@swag_from('./docs/bitrix/market_symbol.yml')
def get_market_summary():
    market_symbol = request.args.get("market")
    if not market_symbol:
        return jsonify({"error": "Market symbol not provided."}), HTTP_400_BAD_REQUEST
    response = requests.get(f"{BITTREX_API_BASE_URL}/markets/{market_symbol}/summary")
    return jsonify(response.json()), HTTP_200_OK
