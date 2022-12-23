content_st = """
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from typing import List, Dict, Tuple

from {{ project_name }}.app.schemas.schemas import ItemSchema, ItemUpdateSchema
from {{ project_name }}.internal.db.db import items
from {{ project_name }}.app.main_manager import MainManager as mm

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema) # schema check when data send to client
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema) # schema check when data receive from client
    @blp.response(200, ItemSchema) # schema check when data send to client
    def put(self, item_data, item_id): # item_data is a json
        try:
            item = items[item_id]

            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            # item |= item_data # python 3.9 or later
            item = {**item, **item_data} # python 3.8 or before

            items[item_id] = item

            return item
        except KeyError:
            abort(404, message="Item not found.")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) # many=True when you are returning a list of elements
    def get(self):
        return [v for k, v in items.items()]

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        for k, item in items.items():
            if (item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]):
                abort(400, message=f"Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item
"""
