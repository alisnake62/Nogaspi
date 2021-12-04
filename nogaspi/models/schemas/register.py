from marshmallow import Schema, fields, INCLUDE, ValidationError

class LoginInputShema(Schema):
    mail = fields.Str(required=True)
    password = fields.Str(required=True)