from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, RegisterException, getArgs
from facades.utils.registerUtils import getUserFromToken


def deleteMyDonations(request):

    token, idDonations = getArgs(request, ['token', 'idDonations'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        for idDonation in idDonations:
            donation = session.query( Donation ).filter(Donation.id == idDonation).first()
            if not donation:
                message = "This donation is not present in Database"
                raise EmptyException(message, message, request)

            if donation.user != user:
                message = "You are not the owner of this donation"
                raise RegisterException(message, message, request)

            donation.checkValidityRaiseException(request)

        for idDonation in idDonations:
            donation.archive = True

        session.commit()

        data = {'isDelete (Archived)':True}

    return data