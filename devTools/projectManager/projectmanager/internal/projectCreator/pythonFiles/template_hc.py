content_st = """
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from typing import List, Dict, Tuple
from datetime import datetime

from {{ project_name }}.app.restful_api.schemas.schemas import HCSchema
from {{ project_name }}.internal.db.db import items
from {{ project_name }}.app.restful_api.main_manager import MainManager as mm

blp = Blueprint("healthcheck", __name__, description="General health checking")

@blp.route("/healthcheck")
class Healthcheck(MethodView):
    @blp.response(200, HCSchema) # schema check when data send to client
    def get(self):
        try:
            return {"status": "Good"
                    , "timestamp": str(datetime.utcnow())}
        except KeyError:
            abort(404, message={"status": "Bad"
                                , "timestamp": str(datetime.utcnow())})
"""
