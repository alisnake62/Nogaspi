from models.objectDB import Conversation
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.firebaseMessages.messageReaded import messageReaded as fbMessage_messageReaded

def acknowledgeMessagesOnConversation(request):

    token, idConversation = getArgs(request, ['token', 'idConversation'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        conversation = session.query( Conversation ).filter(Conversation.id == idConversation).first()
        if not conversation:
            message = "This conversation is not present in Database"
            raise EmptyException(message, message, request)
        
        conversation.checkLegitimacyRaiseException(user, True, request)

        for message in conversation.messages:
            if message.toDonator:
                if user == conversation.userDonator:
                    message.readed = True
                    fbMessage_messageReaded(conversation.userTaker, conversation)
            else:
                if user == conversation.userTaker:
                    message.readed = True
                    fbMessage_messageReaded(conversation.userDonator, conversation)

        session.commit()

        data = {'acknowledge':True}

    return data