from marshmallow import Schema, fields

class WatchRequestSchema(Schema):
    name = fields.Str(required=True)
    brand = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)

class WatchResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    brand = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)