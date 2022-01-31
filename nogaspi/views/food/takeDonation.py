from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.utils.donationUtils import makeDonation

def takeDonation(request):

    token, idDonation, donationCode = getArgs(request, ['token', 'idDonation', 'donationCode'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donation = session.query( Donation ).filter(Donation.id == idDonation).first()
        if not donation:
            message = "This donation is not present in Database"
            raise EmptyException(message, message, request)
        
        donation.checkValidityRaiseException(request)
        donation.compareCodeRaiseException(donationCode, request)

        userOwner = donation.user
        if user == userOwner:
            message = "You can't take your own donation"
            raise DonationException(message, message, request)

        makeDonation(userOwner, user, donation)

        session.commit()

        data = {'isTaked':True}

    return data