from models.objectDB import Donation, Article, Fridge
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.const import EXPIRATION_DATE_TOLERANCE_IN_DAY
import datetime
from facades.utils.donationUtils import sendFireBaseNotificationsOneNewNearDonation



def postDonationFromFridge(request):

    token, idArticles, latitude, longitude, geoPrecision, endingDate = getArgs(request, [
        'token',
        'idArticles',
        'latitude',
        'longitude',
        'geoPrecision',
        'endingDate'
    ])
    latitude, longitude, geoPrecision = (float(f) for f in (latitude, longitude, geoPrecision))

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        if datetime.datetime.fromisoformat(endingDate) < datetime.datetime.now():
            message = "The given endingDate is not valid"
            raise DonationException(message, message, request)
        
        fridge = session.query( Fridge ).filter(Fridge.user == user).first()
        if not fridge: 
            fridge = Fridge(user)
            session.add(fridge)

        donation = Donation(user, latitude, longitude, geoPrecision, endingDate)

        for idArticle in idArticles:
            article = session.query( Article ).filter(Article.id == idArticle).first()
            if not article: 
                message = f"The article {idArticle} is unknow"
                raise EmptyException(message, message, request)

            if datetime.datetime.combine(article.expirationDate, datetime.datetime.min.time()) < datetime.datetime.now() - datetime.timedelta(days=EXPIRATION_DATE_TOLERANCE_IN_DAY):
                message = f"The article {idArticle} is expired"
                raise DonationException(message, message, request)

            if article.idFridge != fridge.id:
                message = f"The article {idArticle} is not in your fridge"
                raise DonationException(message, message, request)

            if article.donation is not None:
                message = f"The article {idArticle} is already in donation"
                raise DonationException(message, message, request)

            article.donation = donation

        session.add(donation)
        session.commit()

        sendFireBaseNotificationsOneNewNearDonation(session, donation)

        data = {'isPosted':True, 'newDonationId': donation.id}

    return data