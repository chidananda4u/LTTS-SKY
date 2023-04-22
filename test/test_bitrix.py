import unittest
from unittest.mock import patch
from flask import Flask
from datetime import datetime, timedelta
import os
import sys
import jwt
from requests.exceptions import RequestException
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.bitrix import bitrix,get_market_summaries, get_market_summary
from src import create_app

app = Flask(__name__)
secret_key = os.environ.get("SECRET_KEY")
app.config['SECRET_KEY'] = secret_key
app.testing = True
client = app.test_client()

@patch('src.bitrix.requests.get')
def test_get_market_summaries(mock_get):
    mock_response = {'key': 'value'}
    mock_get.return_value.status_code ={'key': 'value'}, 200
    exp_time = datetime.utcnow() + timedelta(seconds=1800)
    token = jwt.encode(
        {"user": "test", "exp": exp_time},
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    headers = {
        'x-access-tokens':token
    }
    response = client.get('/api/v1/market/summaries', headers=headers)
    assert response.status_code == 200
    assert response.json == mock_response

@patch('src.bitrix.requests.get')
def test_get_market_summaries_500_error(mock_get):
    mock_get.side_effect = RequestException("500 Internal Server Error")
    exp_time = datetime.utcnow() + timedelta(seconds=1800)
    token = jwt.encode(
        {"user": "test", "exp": exp_time},
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    headers = {
        'x-access-tokens':token
    }
    response = app.test_client().get('/api/v1/market/summaries', headers=headers)
    assert response.status_code == 500

@patch('src.bitrix.requests.get')
def test_get_market_summary(mock_get):
    mock_response = {'key': 'value'}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    response = client.get('/api/v1/markets/summary?market=LTC-BTC')
    assert response.status_code == 200
    assert response.json == mock_response

@patch("src.bitrix.requests.get")
def test_get_market_summary_missing_market_symbol(mock_requests_get):
    mock_requests_get.return_value = MagicMock()
    response = client.get("/api/v1/markets/summary")
    assert response.status_code == 400
    

@patch("app.requests.get")
def test_get_market_summary_invalid_market_symbol(self, mock_requests_get):
    market_symbol = "INVALID-SYMBOL"
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": "Invalid market symbol"}
    mock_requests_get.return_value = mock_response
    response = client.get(f"/api/v1/markets/summary?market={market_symbol}")
    assert response.status_code == 400
    





