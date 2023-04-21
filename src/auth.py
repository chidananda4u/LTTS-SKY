import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import Blueprint, current_app, jsonify, request
from flasgger import swag_from
from .constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)

secret_key = os.environ.get("SECRET_KEY")
load_dotenv()
auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.route("/generate_token", methods=["GET"])
@swag_from('./docs/auth/auth.yml')
def generate_token():
    exp_time = datetime.utcnow() + timedelta(seconds=1800)
    token = jwt.encode(
        {"user": "test", "exp": exp_time},
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify({"token": token.decode("utf-8"), "expire": exp_time}), HTTP_200_OK


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]
        if not token:
            return jsonify({"Alert!": "Token is missing!"}), HTTP_401_UNAUTHORIZED

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"])
            current_user = data["user"]

        except:
            return jsonify({"Message": "Invalid token"}), HTTP_401_UNAUTHORIZED
        return func(*args, **kwargs)

    return decorated
