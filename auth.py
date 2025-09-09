from marshmallow import Schema, fields

class RegisterUserRequestSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
    password_confirm = fields.Str(required=True)
    email = fields.Email(required=True)
class RegisterUserResponseSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginRequestSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)

class LoginResponseSchema(Schema):
    user_name = fields.Str(required=True)
    token = fields.Str(required=True)