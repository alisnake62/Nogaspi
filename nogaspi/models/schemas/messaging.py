from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class InitiateConversationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    firstMessage = fields.Str(required=True)
    idDonation = fields.Int(require = True)

class PostMessageInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    body = fields.Str(required=True)
    idConversation = fields.Int(require = True)

class AcknowledgeMessagesOnConversationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idConversation = fields.Int(require = True)