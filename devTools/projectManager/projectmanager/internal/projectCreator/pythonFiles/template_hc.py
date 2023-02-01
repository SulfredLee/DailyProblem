content_st = """
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from typing import List, Dict, Tuple
from datetime import datetime
import subprocess
from pathlib import Path

from {{ project_name }}.app.{{ app_subfolder }}.schemas.schemas import HCSchema
from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm

blp = Blueprint("healthcheck", __name__, description="General health checking")

@blp.route("/healthcheck")
class Healthcheck(MethodView):
    @blp.response(200, HCSchema) # schema check when data send to client
    def get(self):
        try:
            # # healthcheck for grpc
            # the_output = subprocess.check_output(["bash", "./healthcheck.sh"]
            #                                      , cwd=Path.joinpath(Path(__file__).parent.absolute()
            #                                                          , ".."
            #                                                          , ".."
            #                                                          , "grpc_api"))
            # if "GRPC server is not healthy" in str(the_output):
            #     abort(404, message={"status": "Bad"
            #                         , "timestamp": str(datetime.utcnow())})
            return {"status": "Good"
                    , "timestamp": str(datetime.utcnow())}
        except KeyError:
            abort(404, message={"status": "Bad"
                                , "timestamp": str(datetime.utcnow())})
"""
