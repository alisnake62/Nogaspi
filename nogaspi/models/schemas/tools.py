from marshmallow import Schema, fields, INCLUDE, validate

class GetProfilePictureInputSchema(Schema):
    idUser = fields.Int(require = True)