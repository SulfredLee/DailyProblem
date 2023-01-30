content_st = """
from flask import Flask, render_template, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from typing import List, Dict, Tuple
import datetime

from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm
from {{ project_name }}.app.{{ app_subfolder }}.schemas.schemas import BlogpostSchema

blp = Blueprint("Home", __name__, description="Home page of {{ project_name }}")

@blp.route("/")
class Home(MethodView):
    def get(self):
        try:
            return render_template("home.html", entries=mm.instance().get_all_blog_post())
        except KeyError:
            abort(404, message="Item not found.")

    def post(self):
        try:
            form = BlogpostSchema()
            if form.validate_on_submit():
                entry_content = form.data.get("content")
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
                mm.instance().save_a_blog_post({"content": entry_content, "date": formatted_date})
            else:
                print(form.errors)
            return render_template("home.html", entries=mm.instance().get_all_blog_post())
        except KeyError:
            abort(404, message="Item not found.")
"""
