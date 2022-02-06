from models.objectDB import Donation, DonationCode
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.utils.donationUtils import makeDonation

def takeDonations(request):

    token, donationCode = getArgs(request, ['token', 'donationCode'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donationCode = session.query( DonationCode ).filter(DonationCode.code == donationCode).first()
        if not donationCode:
            message = "This donationCode is not present in Database"
            raise EmptyException(message, message, request)

        if not donationCode.isValide():
            message = "This donationCode is expired"
            raise EmptyException(message, message, request)

        if donationCode.userOwner() == user:
            message = "You can't take your own donations"
            raise EmptyException(message, message, request)
        
        for donation in donationCode.donations:
            makeDonation(donation.user, user, donation)

        session.commit()

        data = {'isTaked':True}

    return data