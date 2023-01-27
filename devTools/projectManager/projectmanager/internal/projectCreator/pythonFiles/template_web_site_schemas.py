content_st = """
from marshmallow import Schema, fields
'''
For Flask form validation, here is an example:
https://www.digitalocean.com/community/tutorials/how-to-use-and-validate-web-forms-with-flask-wtf#step-4-accessing-form-data
'''
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField)
from wtforms.validators import InputRequired, Length

class BlogpostSchema(FlaskForm):
    content = StringField("content", validators=[InputRequired()
                                                 , Length(min=10, max=1024)])

class HCSchema(Schema):
    status = fields.Str(required=True)
    timestamp = fields.Str(required=True)
"""
