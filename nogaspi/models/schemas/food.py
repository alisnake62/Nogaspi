from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class GetProductInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    barcode = fields.Str(required=True, validate = validate.Length(max=20, error='Your barcode has not a good format'))

class PostDonationFromScanInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    articles = fields.List(fields.Nested(Schema.from_dict(
        {
            'barcode': fields.Str(required=True, validate = validate.Length(max=20, error='Your barcode has not a good format')),
            'expirationDate': fields.Date(required = True)
        })), validate = validate.Length(1,100), require = True)
    latitude = fields.Float(validate=validate.Range(min=-90.0, max=90.0), require = True)
    longitude = fields.Float(validate=validate.Range(min=-180.0, max=180.0), require = True)
    geoPrecision = fields.Int(require = True)
    endingDate = fields.Date(required = True)

class PostDonationFromFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    articles = fields.List(fields.Nested(Schema.from_dict(
        {
            'id': fields.Int(require = True)
        })), validate = validate.Length(1,100), require = True)
    latitude = fields.Float(validate=validate.Range(min=-90.0, max=90.0), require = True)
    longitude = fields.Float(validate=validate.Range(min=-180.0, max=180.0), require = True)
    geoPrecision = fields.Int(require = True)
    endingDate = fields.Date(required = True)

class DeleteMyDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonations = fields.List(fields.Int(require = True), validate = validate.Length(1,1000), require = True)

class GetDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    latitude = fields.Float(validate=validate.Range(min=-90.0, max=90.0))
    longitude = fields.Float(validate=validate.Range(min=-180.0, max=180.0))
    distanceMax = fields.Int()

class GetDonationsByRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    distanceMax = fields.Int(require = True)

class GetAllergensInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))

class PostArticlesInFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    articles = fields.List(fields.Nested(Schema.from_dict(
        {
            'barcode': fields.Str(required=True, validate = validate.Length(max=20, error='Your barcode has not a good format')),
            'expirationDate': fields.Date(required = True)
        })), validate = validate.Length(1,1000), require = True)

class DeleteArticlesInFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idArticles = fields.List(fields.Int(require = True), validate = validate.Length(1,1000), require = True)

class GetArticlesInFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))

class TakeDonationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonation = fields.Int(require = True)
    donationCode = fields.Str(required=True, validate = validate.Length(equal=64, error='Donation Code must have 64 characters'))
    
class GetDonationCodeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonation = fields.Int(require = True)

class GetFavoriteDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))

class ToggleDonationInMyFavoriteInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonation = fields.Int(require = True)

class GetMyDonationCodeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    withArchived = fields.Bool(require = True)
    withExpired = fields.Bool(require = True)