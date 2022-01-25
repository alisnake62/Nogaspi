from marshmallow import Schema, fields, INCLUDE, validate

class GetProfilePictureInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))