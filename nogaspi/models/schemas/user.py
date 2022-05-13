from fileinput import filename
from unicodedata import name
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

class SetMyInfosInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    address = fields.Str(required=True, allow_none=True)
    idAllergen = fields.Int(required = True, allow_none=True)
    favoriteDistanceToSearch = fields.Int(required = True, allow_none=True)
    favoriteGeoPrecisionToDonate = fields.Int(required = True, allow_none=True)

class FilePostProfilePicture(Schema):
    profilePicture = fields.Field(
        validate=lambda file: file.filename.split(".")[-1].lower() in ('jpg', 'jpeg', 'bnp'),
        location="files",
        required=True
    )

class PostProfilePicture(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))