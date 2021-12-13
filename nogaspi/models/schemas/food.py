from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class GetProductInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    barcode = fields.Str(required=True, validate = validate.Length(max=20, error='Your barcode has not a good format'))

class PostDonationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    articles = fields.List(fields.Nested(Schema.from_dict(
        {
            'barcode': fields.Str(required=True, validate = validate.Length(max=20, error='Your barcode has not a good format')),
            'expirationDate': fields.Date(required = True)
        })), validate = validate.Length(1,100))
    latitude = fields.Float(require = True)
    longitude = fields.Float(require = True)
    geoPrecision = fields.Int(require = True)
    endingDate = fields.Date(required = True)

class GetDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    latitude = fields.Float()
    longitude = fields.Float()
    geoPrecision = fields.Int()

class GetAllergensInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))

class PostArticlesInFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    articles = fields.List(fields.Nested(Schema.from_dict(
        {
            'barcode': fields.Str(required=True, validate = validate.Length(max=20, error='Your barcode has not a good format')),
            'expirationDate': fields.Date(required = True)
        })), validate = validate.Length(1,100))

class GetArticlesInFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))