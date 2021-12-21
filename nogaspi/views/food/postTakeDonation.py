from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException
from facades.registerUtils import getUserFromToken
from facades.donationUtils import checkDonationCode

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

        checkDonationCode(donation, donationCode, request)

        userDonation = donation.user

        session.delete(donation)
        user.points += 5
        userDonation.points += 20
        
        session.commit()

        data = {'isTaked':True}

    return data