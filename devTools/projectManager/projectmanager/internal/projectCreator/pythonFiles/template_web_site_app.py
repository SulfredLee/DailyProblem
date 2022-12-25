content_st = """
import logging
from typing import List, Dict, Tuple
from flask import Flask
from flask_smorest import Api
import sfdevtools.observability.log_helper as lh

from {{ project_name }}.app.routes.home import blp as HomeBlueprint
from {{ project_name }}.app.routes.authen import blp as AuthenBlueprint
from {{ project_name }}.app.routes.bootstrap_example import blp as BootstrapExampleBlueprint
from {{ project_name }}.app.main_manager import MainManager as mm

class Config:
    API_TITLE = "{{ project_name }} REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

def create_app():
    main_m = mm.instance()
    logger = main_m.get_logger()

    # Create flask app
    app = Flask(__name__)
    # Secret key generated with secrets.token_urlsafe()
    app.secret_key = "lkaQT-kAb6aIvqWETVcCQ28F-j-rP_PSEaCDdTynkXA"

    app.config.from_object(Config)

    # Create restful api object
    api = Api(app)

    # Initial database
    with app.app_context():
        logger.info("You can now initial your database within the application context life cycle.")

    # Register blueprint
    api.register_blueprint(HomeBlueprint)
    api.register_blueprint(AuthenBlueprint)
    api.register_blueprint(BootstrapExampleBlueprint)

    return app
"""
