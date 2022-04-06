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
        })), validate = validate.Length(1,100), required = True)
    latitude = fields.Float(validate=validate.Range(min=-90.0, max=90.0), required = True)
    longitude = fields.Float(validate=validate.Range(min=-180.0, max=180.0), required = True)
    geoPrecision = fields.Int(required = True)
    visibilityOnMap = fields.Str(required = True, validate = validate.OneOf(['0', '1']))
    endingDate = fields.Date(required = True)

class PostDonationFromFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idArticles = fields.List(fields.Int(required = True), required = True, validate = validate.Length(1,1000))
    latitude = fields.Float(validate=validate.Range(min=-90.0, max=90.0), required = True)
    longitude = fields.Float(validate=validate.Range(min=-180.0, max=180.0), required = True)
    geoPrecision = fields.Int(required = True)
    visibilityOnMap = fields.Str(required = True, validate = validate.OneOf(['0', '1']))
    endingDate = fields.Date(required = True)

class DeleteMyDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonations = fields.List(fields.Int(required = True), required = True, validate = validate.Length(1,1000))

class GetDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    latitude = fields.Float(required = True, validate=validate.Range(min=-90.0, max=90.0))
    longitude = fields.Float(required = True, validate=validate.Range(min=-180.0, max=180.0))
    distanceMax = fields.Int(required = True)

class GetDonationByIdInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonation = fields.Int(required = True)

class GetDonationsByRegularPathInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    distanceMax = fields.Int(required = True)

class GetAllergensInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))

class PostArticlesInFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    articles = fields.List(fields.Nested(Schema.from_dict(
        {
            'barcode': fields.Str(required=True, validate = validate.Length(max=20, error='Your barcode has not a good format')),
            'expirationDate': fields.Date(required = True)
        })), validate = validate.Length(1,1000), required = True)

class DeleteArticlesInFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idArticles = fields.List(fields.Int(required = True), required = True, validate = validate.Length(1,1000))

class GetArticlesInFridgeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))

class TakeDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    donationCode = fields.Str(required=True, validate = validate.Length(equal=64, error='Donation Code must have 64 characters'))
    
class GenerateDonationsCodeInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonations = fields.List(fields.Int(required = True), required = True, validate = validate.Length(1,1000))

class GetFavoriteDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))

class ToggleDonationInMyFavoriteInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonation = fields.Int(required = True)

class GetMyDonationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    withArchived = fields.Str(required = True, validate = validate.OneOf(['0', '1']))
    withExpired = fields.Str(required = True, validate = validate.OneOf(['0', '1']))

class RateDonationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonation = fields.Int(required = True)
    note = fields.Int(required = True, validate=validate.Range(min=0, max=5))