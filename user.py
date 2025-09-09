from marshmallow import Schema, fields

class UserRequestSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True) 
    role = fields.Str(required=True)
class UserResponseSchema(Schema):
    user_id = fields.Int(required=True)
    user_name = fields.Str(required=True)
    email = fields.Email(required=True) 
    role = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)
    token = fields.Str(required=True)
