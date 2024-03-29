from marshmallow import Schema, fields, INCLUDE, ValidationError, validate

class InitiateConversationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    firstMessage = fields.Str(required=True, validate = validate.Length(min=1, max=2000, error='The message should not have more than 2000 characters'))
    idDonation = fields.Int(required = True)

class PostMessageInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    body = fields.Str(required=True, validate = validate.Length(min=1, max=2000, error='The message should not have more than 2000 characters'))
    idConversation = fields.Int(required = True)

class AcknowledgeMessagesOnConversationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idConversation = fields.Int(required = True)

class GetMyConversationsInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    withArchivedDonations = fields.Str(required = True, validate = validate.OneOf(['0', '1']))
    withExpiredDonations = fields.Str(required = True, validate = validate.OneOf(['0', '1']))

class GetConversationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idConversation = fields.Int(required = True)

class GetConversationsByDonationInputSchema(Schema):
    token = fields.Str(required=True, validate = validate.Length(equal=64, error='Token must have 64 characters'))
    idDonation = fields.Int(required = True)