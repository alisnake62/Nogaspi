from models.objectDB import Conversation
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException, ConversationException
from facades.registerUtils import getUserFromToken

def f(request):

    token = request.json['token']
    idConversation = request.json['idConversation']

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        conversation = session.query( Conversation ).filter(Conversation.id == idConversation).first()
        if not conversation:
            message = "This conversation is not present in Database"
            raise EmptyException(message, message, request)
        
        conversation.checkLegitimacyRaiseException(user, request)

        for message in conversation.messages:
            if message.toDonator:
                if user == conversation.userDonator:
                    message.readed = True
            else:
                if user == conversation.userTaker:
                    message.readed = True

        session.commit()

        data = {'acknowledge':True}

    return data