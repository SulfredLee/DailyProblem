from jsonschema import validate
from jschon import create_catalog, JSON, JSONSchema
import json
import os

schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
    "required": [
        "name"
    ]
}

validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

future_data = None
future_schema = None
with open(os.path.join(os.path.dirname(os.path.realpath(__file__))
                       , "future_ult.json")) as json_file:
    future_data = json.load(json_file)

with open(os.path.join(os.path.dirname(os.path.realpath(__file__))
                       , "ult_schema.json")) as json_file:
    future_schema = json.load(json_file)


# Try jsonschema
validate(instance=future_data, schema=future_schema)
