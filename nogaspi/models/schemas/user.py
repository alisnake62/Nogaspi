from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class PostRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    latitudeStart = fields.Float(validate=validate.Range(min=-90.0, max=90.0), require = True)
    longitudeStart = fields.Float(validate=validate.Range(min=-180.0, max=180.0), require = True)
    latitudeEnd = fields.Float(validate=validate.Range(min=-90.0, max=90.0), require = True)
    longitudeEnd = fields.Float(validate=validate.Range(min=-180.0, max=180.0), require = True)
    pathPoints = fields.List(fields.Nested(Schema.from_dict(
    {
        'latitude': fields.Float(validate=validate.Range(min=-90.0, max=90.0), require = True),
        'longitude': fields.Float(validate=validate.Range(min=-180.0, max=180.0), require = True)
    })), validate = validate.Length(1,5000), require = True)

class GetRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    