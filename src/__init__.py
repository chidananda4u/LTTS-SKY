import os

from flasgger import Swagger, swag_from

from flask import Flask, config, redirect

from . import auth, bitrix
from src.config.swagger import template, swagger_config


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            BITTREX_API_BASE_URL = os.environ.get("BITTREX_API_BASE_URL"),
            
            SWAGGER={
                    'title': "Bitrix API",
                    'uiversion': 3
                }
        )
    else:
        app.config.from_mapping(test_config)

    
    app.register_blueprint(auth.auth)
    app.register_blueprint(bitrix.bitrix)

    Swagger(app, config=swagger_config, template=template)
    
    return app