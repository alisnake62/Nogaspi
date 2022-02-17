from models.objectDB import Donation, FavoriteDonation
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, getArgs
from facades.utils.registerUtils import getUserFromToken

import sys
import traceback

def toggleDonationInMyFavorite(request):

    token, idDonation = getArgs(request, ['token', 'idDonation'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donation = session.query( Donation ).filter(Donation.id == idDonation).first()
        if not donation:
            message = "This donation is not present in Database"
            raise EmptyException(message, message, request)
        
        if donation.user == user:
            message = "This donation is yours"
            raise DonationException(message, message, request)
        
        donation.checkValidityRaiseException(request)

        row = session.query(FavoriteDonation).filter(
            FavoriteDonation.idUser == user.id,
            FavoriteDonation.idDonation == donation.id
        ).first()

        if not row:
            session.add(FavoriteDonation(user.id, donation.id))
            try:
                donation.user.sendFireBaseNotification(user.id, "Donation", f"{user.pseudo} aime votre donation")
            except Exception as err:
                print(traceback.format_exc(), file = sys.stderr )
        else:
            session.delete(row)

        session.commit()

        data = {'isFavorite':donation.isFavorite(user)}

    return data