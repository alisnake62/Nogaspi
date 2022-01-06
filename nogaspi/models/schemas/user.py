from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class PostRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    latitude1 = fields.Float(validate=validate.Range(min=-90.0, max=90.0), require = True)
    longitude1 = fields.Float(validate=validate.Range(min=-180.0, max=180.0), require = True)
    latitude2 = fields.Float(validate=validate.Range(min=-90.0, max=90.0), require = True)
    longitude2 = fields.Float(validate=validate.Range(min=-180.0, max=180.0), require = True)

class GetRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))