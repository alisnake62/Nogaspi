from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class GetArticleInputShema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    barcode = fields.Str(required=True)

