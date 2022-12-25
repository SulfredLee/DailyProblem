content_st = """
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from typing import List, Dict, Tuple
import functools
from flask import (
    Flask,
    session,
    render_template,
    request,
    abort,
    flash,
    redirect,
    url_for,
)


from microblog.app.main_manager import MainManager as mm

route_name = "Bootstrap_Example"
blp = Blueprint(route_name, __name__, description="Page for authentication demo")

@blp.get("/bootstrap_example")
def bootstrap_example():
    return render_template("bootstrap_example.html")
"""
