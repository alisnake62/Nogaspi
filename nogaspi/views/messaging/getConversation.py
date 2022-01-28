from models.objectDB import Conversation
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException, getArgs
from facades.registerUtils import getUserFromToken

def f(request):

    token, idConversation = getArgs(request, ['token', 'idConversation'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        conversation = session.query( Conversation ).filter(Conversation.id == idConversation).first()
        if not conversation:
            message = "This conversation is not present in Database"
            raise EmptyException(message, message, request)
        
        data = {'conversation': conversation.toJson(user)}

    return data