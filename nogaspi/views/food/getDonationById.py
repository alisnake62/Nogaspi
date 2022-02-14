from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs, EmptyException

def getDonationById(request):

    token, idDonation = getArgs(request, ['token', 'idDonation'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        donation = session.query( Donation ).filter(Donation.id == idDonation).first()
        if not donation:
            message = "The donation are not present in Database"
            raise EmptyException(message, message, request)

        data = {'donation': donation.toJson(user)}
    return data