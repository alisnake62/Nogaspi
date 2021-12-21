from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException, DonationException
from facades.registerUtils import getUserFromToken
from facades.donationUtils import makeDonation

def f(request):

    token = request.json['token']
    idDonation = request.json['idDonation']
    donationCode = request.json['donationCode']

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