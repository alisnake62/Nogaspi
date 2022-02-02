from models.objectDB import Conversation, Message
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, getArgs
from facades.utils.registerUtils import getUserFromToken

def postMessage(request):

    token, idConversation, body = getArgs(request, ['token', 'idConversation', 'body'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        conversation = session.query( Conversation ).filter(Conversation.id == idConversation).first()
        if not conversation:
            message = "This conversation is not present in Database"
            raise EmptyException(message, message, request)
        
        conversation.checkLegitimacyRaiseException(user, True, request)

        toDonator = False if user == conversation.donation.user else True
        
        message = Message(conversation, toDonator, body)
        session.add(message)

        session.commit()

        data = {'posted':True}

    return data