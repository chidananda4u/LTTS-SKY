import os
import sys
from datetime import datetime, timedelta
from unittest.mock import patch

import jwt
from flask import Flask
from requests.exceptions import RequestException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.bitrix import bitrix

app = Flask(__name__)
secret_key = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = secret_key
app.testing = True
client = app.test_client()
exp_time = datetime.utcnow() + timedelta(seconds=1800)
token = jwt.encode(
    {"user": "test", "exp": exp_time},
    app.config["SECRET_KEY"],
    algorithm="HS256",
)
headers = {"x-access-tokens": token}


@patch("src.bitrix.requests.get")
def test_get_market_summaries(mock_get):
    '''unit test to test get request of market summaries'''
    mock_response = {"key": "value"}
    mock_get.return_value.status_code = {"key": "value"}, 200
    response = client.get("/api/v1/market/summaries", headers=headers)
    assert response.status_code == 200
    assert response.json == mock_response


@patch("src.bitrix.requests.get")
def test_get_market_summaries_500_error(mock_get):
    '''unit test to test get request with server error of market summaries'''
    mock_get.side_effect = RequestException("500 Internal Server Error")
    response = app.test_client().get("/api/v1/market/summaries", headers=headers)
    assert response.status_code == 500


@patch("src.bitrix.requests.get")
def test_get_market_summary(mock_get):
    '''unit test to test get request of market symbol'''
    mock_response = {"key": "value"}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    response = client.get("/api/v1/markets/summary?market=LTC-BTC", headers=headers)
    assert response.status_code == 200
    assert response.json == mock_response


@patch("src.bitrix.requests.get")
def test_get_market_summary_missing_market_symbol(mock_requests_get):
    '''unit test to test get request of market symbol without passing parameter'''
    mock_requests_get.return_value = MagicMock()
    response = client.get("/api/v1/markets/summary", headers=headers)
    assert response.status_code == 400


@patch("src.bitrix.requests.get")
def test_get_market_summary_invalid_market_symbol(mock_requests_get):
    '''unit test to test get request of market symbol by passing invalid param'''
    market_symbol = "INVALID-SYMBOL"
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": "Invalid market symbol"}
    mock_requests_get.return_value = mock_response
    response = client.get(
        f"/api/v1/markets/summary?market={market_symbol}", headers=headers
    )
    assert response.status_code == 400
