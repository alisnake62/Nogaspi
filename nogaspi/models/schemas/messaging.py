from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class InitiateConversationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    firstMessage = fields.Str(required=True, validate = validate.Length(max=2000, error='The message should not have more than 800 characters'))
    idDonation = fields.Int(require = True)

class PostMessageInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    body = fields.Str(required=True, validate = validate.Length(max=2000, error='The message should not have more than 800 characters'))
    idConversation = fields.Int(require = True)

class AcknowledgeMessagesOnConversationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idConversation = fields.Int(require = True)

class GetMyConversationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    withArchivedDonations = fields.Str(require = True, validate = validate.OneOf(['0', '1']))
    withExpiredDonations = fields.Str(require = True, validate = validate.OneOf(['0', '1']))

class GetConversationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idConversation = fields.Int(require = True)

class GetConversationsByDonationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonation = fields.Int(require = True)