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
from passlib.hash import pbkdf2_sha256

from {{ project_name }}.app.{{ app_subfolder }}.main_manager import MainManager as mm
from {{ project_name }}.internal.db.db import users

route_name = "Authen"
blp = Blueprint(route_name, __name__, description="Page for authentication demo")

def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(f"{route_name}.login"))

        return route(*args, **kwargs)

    return route_wrapper


@blp.get("/protected")
@login_required
def protected():
    return render_template("protected.html")


@blp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if pbkdf2_sha256.verify(password, users.get(email)):
            session["email"] = email
            return redirect(url_for(f"{route_name}.protected"))
        else:
            abort(401)
    return render_template("login.html")


@blp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        users[email] = pbkdf2_sha256.hash(password)
        # session["email"] = email
        # - Setting the session here would be okay if you
        # - want users to be logged in immediately after
        # - signing up.
        flash("Successfully signed up.")
        return redirect(url_for(f"{route_name}.login"))
    return render_template("signup.html")


@blp.errorhandler(401)
def auth_error():
    return "Not authorized"
"""
