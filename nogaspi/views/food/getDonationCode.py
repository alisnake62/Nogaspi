from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException, RegisterException
from facades.registerUtils import getUserFromToken


def f(request):

    token = request.args.get('token')
    idDonation = request.args.get('idDonation')

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        donation = session.query( Donation ).filter(Donation.id == idDonation).first()
        if not donation:
            message = "This donation is not present in Database"
            raise EmptyException(message, message, request)
        
        if donation.user != user:
            message = "You are not the owner of this donation"
            raise RegisterException(message, message, request)

        donationCodeInfo = donation.generateCode()
        session.commit()

    return donationCodeInfo