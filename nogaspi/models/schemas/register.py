from marshmallow import Schema, fields, INCLUDE, validate

class CreateUserInputSchema(Schema):
    mail = fields.Str(required=True, validate = validate.Email(error='The mail address is not valid'))
    password = fields.Str(required=True, validate = validate.Length(max=200, error='Password must have less than 200 characters'))
    pseudo = fields.Str(required=True, validate = validate.Length(max=200, error='Pseudo must have less than 50 characters'))

class ConfirmUserCreationInputSchema(Schema):
    mail = fields.Str(required=True)
    confirmationCode = fields.Str(required=True, validate = validate.Length(equal=10, error='Confirmation Code must have 10 characters'))

class LoginInputSchema(Schema):
    mail = fields.Str(required=True)
    password = fields.Str(required=True)

class LogoutInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))

class CheckTokenValidityInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))