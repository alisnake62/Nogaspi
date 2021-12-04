from marshmallow import Schema, fields, INCLUDE, ValidationError

class GetArticleInputShema(Schema):
    token = fields.Str(required=True)
    barcode = fields.Str(required=True)

