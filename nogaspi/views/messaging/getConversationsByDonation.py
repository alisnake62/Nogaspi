from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, getArgs
from facades.utils.registerUtils import getUserFromToken

def getConversationsByDonation(request):

    token, idDonation = getArgs(request, ['token', 'idDonation'])
    
    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donation = session.query( Donation ).filter(Donation.id == idDonation).first()
        if not donation:
            message = "This donation is not present in Database"
            raise EmptyException(message, message, request)

        if donation.user != user:
            message = "This donation is not yours"
            raise DonationException(message, message, request)

        data = {'conversations': [c.toJson(user) for c in donation.conversations]}

    return data