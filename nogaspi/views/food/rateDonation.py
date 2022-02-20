from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.utils.donationUtils import updateRatingUser

def rateDonation(request):

    token, idDonation, note = getArgs(request, ['token', 'idDonation', 'note'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        donation = session.query( Donation ).filter(Donation.id == idDonation).first()
        if not donation:
            message = "This donation are not present in Database"
            raise EmptyException(message, message, request)

        if not donation.archive or donation.userTaker is None:
            message = "This donation is not taked"
            raise DonationException(message, message, request)

        if donation.userTaker != user:
            message = "You'r not the taker of this Donation"
            raise DonationException(message, message, request)

        if donation.rating is not None:
            message = "This Donation is Already Rated"
            raise DonationException(message, message, request)

        donation.rating = note
        updateRatingUser(donation.user, note)

        session.commit()

        data = {'isRated':True}

    return data