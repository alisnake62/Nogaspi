from models.objectDB import Donation, FavoriteDonation
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException, DonationException
from facades.registerUtils import getUserFromToken

def f(request):

    token = request.json['token']
    idDonation = request.json['idDonation']

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donation = session.query( Donation ).filter(Donation.id == idDonation).first()
        if not donation:
            message = "This donation is not present in Database"
            raise EmptyException(message, message, request)
        
        donation.checkValidityRaiseException(request)

        row = session.query(FavoriteDonation).filter(
            FavoriteDonation.idUser == user.id,
            FavoriteDonation.idDonation == donation.id
        ).first()

        if not row:
            session.add(FavoriteDonation(user.id, donation.id))
            donation.user.sendFireBaseNotification("Donation", f"{user.pseudo} aime votre donation")
        else:
            session.delete(row)

        session.commit()

        data = {'isFavorite':donation.isFavorite(user)}

    return data