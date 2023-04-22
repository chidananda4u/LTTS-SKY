import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import jwt
from flask import Flask

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.auth import auth


app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_secret_key'
app.register_blueprint(auth)

client = app.test_client()

@patch('src.auth.datetime')
@patch('src.auth.jwt')
def test_generate_token(mock_jwt, mock_datetime):
    mock_datetime.utcnow.return_value = datetime(2023, 4, 21, 12, 0, 0)
    exp_time = datetime.utcnow() + timedelta(seconds=1800)
    mock_jwt.encode.return_value = b'test_token'

    response = client.get('/api/v1/auth/generate_token')
    assert response.status_code == 200
    assert response.json['token'] is not None

    
