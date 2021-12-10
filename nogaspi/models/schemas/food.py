from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class GetArticleInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    barcode = fields.Str(required=True, validate = validate.Length(max=20, error='Your barcode has not a good format'))

class PostDonationWithBarCodeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    barcode = fields.Str(required=True, validate = validate.Length(max=20, error='Your barcode has not a good format'))
    expirationDate = fields.Date(required = True)
    latitude = fields.Float(require = True)
    longitude = fields.Float(require = True)
    geoPrecision = fields.Int(require = True)

class GetDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    latitude = fields.Float()
    longitude = fields.Float()
    geoPrecision = fields.Int()

