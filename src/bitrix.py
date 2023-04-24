import json
import os

import requests
from dotenv import load_dotenv
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from .auth import token_required
from .constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

BITTREX_API_BASE_URL = os.environ.get("BITTREX_API_BASE_URL")
load_dotenv()
bitrix = Blueprint("bitrix", __name__, url_prefix="/api/v1/")


@bitrix.route("/market/summaries", methods=["GET"])
@token_required
@swag_from("./docs/bitrix/market_summaries.yml")
def get_market_summaries():
    """function to get all market summarries"""
    try:
        response = requests.get(f"{BITTREX_API_BASE_URL}/markets/summaries", timeout=30)
        response.raise_for_status()
        return jsonify(response.json()), HTTP_200_OK
    except requests.exceptions.RequestException as err:
        return jsonify({"error": str(err)}), HTTP_500_INTERNAL_SERVER_ERROR


@bitrix.route("/markets/summary", methods=["GET"])
@token_required
@swag_from("./docs/bitrix/market_symbol.yml")
def get_market_summary():
    """function to get only the give  market summary symbol"""
    market_symbol = request.args.get("market")
    if not market_symbol:
        return jsonify({"error": "Market symbol not provided."}), HTTP_400_BAD_REQUEST
    response_of_summaries = requests.get(
        "https://api.bittrex.com/v3/markets/summaries", timeout=5
    )

    data_dict = json.loads(response_of_summaries.content)
    list_0f_market_symbol = []
    for index in data_dict:
        if index["symbol"] not in list_0f_market_symbol:
            list_0f_market_symbol.append(index["symbol"])
    if market_symbol in list_0f_market_symbol:
        response = requests.get(
            f"{BITTREX_API_BASE_URL}/markets/{market_symbol}/summary", timeout=30
        )
        return jsonify(response.json()), HTTP_200_OK
    return jsonify({"code": "MARKET_DOES_NOT_EXIST"}), 404
