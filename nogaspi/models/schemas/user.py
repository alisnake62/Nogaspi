from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class GenerateRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    latitudeStart = fields.Float(validate=validate.Range(min=-90.0, max=90.0), required = True)
    longitudeStart = fields.Float(validate=validate.Range(min=-180.0, max=180.0), required = True)
    latitudeEnd = fields.Float(validate=validate.Range(min=-90.0, max=90.0), required = True)
    longitudeEnd = fields.Float(validate=validate.Range(min=-180.0, max=180.0), required = True)
    pathType = fields.Str(required=True, validate = validate.OneOf(['car', 'bike', 'foot']))

class GetRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    
class PostFireBaseTokenInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    fireBaseToken = fields.Str(required=True, validate = validate.Length(equal=163, error='FireBase Token must have 163 characters'))

class GetMyInfosInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
