content_st = """
import logging
from typing import List, Dict, Tuple
from flask import Flask
from flask_smorest import Api
import sfdevtools.observability.log_helper as lh

from {{ project_name }}.app.{{ app_subfolder }}.routes.item import blp as ItemBlueprint
from {{ project_name }}.app.{{ app_subfolder }}.routes.store import blp as StoreBlueprint
from {{ project_name }}.app.{{ app_subfolder }}.routes.healthcheck import blp as HCBlueprint
from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm

# to start the server
# $ poetry run falsk run

class Config:
    API_TITLE = "{{ project_name }} REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

def create_app():
    logger: logging.Logger = lh.init_logger(logger_name="{{ project_name }}_restful_logger", is_json_output=False)

    main_m = mm.instance()
    main_m.init_component(logger=logger)

    # Create flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Create restful api object
    api = Api(app)

    # Initial database
    with app.app_context():
        logger.info("You can now initial your database within the application context life cycle.")

    # Register blueprint
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(HCBlueprint)

    return app
"""
