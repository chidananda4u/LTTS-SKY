import os
from datetime import datetime, timedelta

from flask import Blueprint, current_app, jsonify, request
from functools import wraps
import jwt
from dotenv import load_dotenv


secret_key = os.environ.get("SECRET_KEY")
load_dotenv()
auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.route("/generate_token", methods=["GET"])
def generate_token():
    exp_time = datetime.utcnow() + timedelta(seconds=1800)
    
    token = jwt.encode(
        {"user": "test", "exp": exp_time},
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify({"token": token.decode("utf-8"), "expire": exp_time})


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
            return jsonify({"Message": "Invalid token"}), HTTP_403_FORBIDDEN
        return func(*args, **kwargs)

    return decorated
