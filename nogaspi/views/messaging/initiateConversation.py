from models.objectDB import Donation, Conversation, Message
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.firebaseMessages.newConversation import newConversation as fbMessage_newConversation

def initiateConversation(request):

    token, idDonation, firstMessage = getArgs(request, ['token', 'idDonation', 'firstMessage'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donation = session.query( Donation ).filter(Donation.id == idDonation).first()
        if not donation:
            message = "This donation is not present in Database"
            raise EmptyException(message, message, request)
        
        donation.checkValidityRaiseException(request)

        userOwner = donation.user
        if user == userOwner:
            message = "You can't initiate a conversation for your own donation"
            raise DonationException(message, message, request)

        for conversation in donation.conversations:
            if conversation.userTaker == user:
                message = "You can't initiate more than one conversation for a donation"
                raise DonationException(message, message, request)
                
        conversation = Conversation(donation, userOwner, user)
        session.add(conversation)

        message = Message(conversation, True, firstMessage)
        session.add(message)

        session.commit()

        fbMessage_newConversation(user, userOwner, conversation, firstMessage)

        data = {'isInitiate':True, 'idNewConversation': conversation.id}

    return data