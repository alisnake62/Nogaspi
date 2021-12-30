from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class PostRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    latitude1 = fields.Float(require = True)
    longitude1 = fields.Float(require = True)
    latitude2 = fields.Float(require = True)
    longitude2 = fields.Float(require = True)

class GetRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))