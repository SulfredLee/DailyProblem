content_st = """
from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Str(dump_only=True) # dump_only: from server to client
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class HCSchema(Schema):
    status = fields.Str(required=True)
    timestamp = fields.Str(required=True)
"""
