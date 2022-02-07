from models.objectDB import Donation, DonationCode
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, RegisterException, getArgs
from facades.utils.registerUtils import getUserFromToken


def generateDonationsCode(request):
    
    token, idDonations = getArgs(request, ['token', 'idDonations'])
    
    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donations = session.query( Donation ).filter(Donation.id.in_(idDonations)).all()
        if not donations or len(donations) != len(idDonations):
            message = "The donations are not present in Database"
            raise EmptyException(message, message, request)
        
        for donation in donations:
            if donation.user != user:
                message = f"You are not the owner of the donation {donation.id}"
                raise RegisterException(message, message, request)
            donation.checkValidityRaiseException(request)

        donationCode = DonationCode()
        for donation in donations:
            donation.donationCode = donationCode

        session.commit()

        data = donationCode.toJson()

    return data