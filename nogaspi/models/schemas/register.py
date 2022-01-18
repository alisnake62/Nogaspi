from marshmallow import Schema, fields, INCLUDE, validate

class LoginInputSchema(Schema):
    mail = fields.Str(required=True)
    password = fields.Str(required=True)

class LogoutInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))

class CheckTokenValidityInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))