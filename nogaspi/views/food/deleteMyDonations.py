from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, RegisterException, getArgs
from facades.utils.registerUtils import getUserFromToken


def deleteMyDonations(request):

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

        for donation in donations:
            donation.archive = True

        session.commit()

    return {'isDelete (Archived)': True}