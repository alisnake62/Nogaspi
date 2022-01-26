from models.objectDB import Donation, Conversation, Message
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException, DonationException
from facades.registerUtils import getUserFromToken

def f(request):

    token = request.json['token']
    idDonation = request.json['idDonation']
    firstMessage = request.json['firstMessage']

    with EngineSQLAlchemy(request) as session:

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