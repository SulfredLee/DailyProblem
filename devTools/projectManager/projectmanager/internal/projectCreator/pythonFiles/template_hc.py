content_st = """
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from typing import List, Dict, Tuple
from datetime import datetime

from peacock.app.schemas.schemas import HCSchema
from peacock.internal.db.db import items
from peacock.app.main_manager import MainManager as mm

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
