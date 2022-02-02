from models.objectDB import Donation, Conversation, Message
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, getArgs
from facades.utils.registerUtils import getUserFromToken

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

        conversation = Conversation(donation, userOwner, user)
        session.add(conversation)

        message = Message(conversation, True, firstMessage)
        session.add(message)

        session.commit()

        data = {'isInitiate':True}

    return data