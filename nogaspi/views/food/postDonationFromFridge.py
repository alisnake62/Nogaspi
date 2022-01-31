from models.objectDB import Donation, Article, Fridge
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.utils.scanUtils import getProductFromWeb


def postDonationFromFridge(request):

    token, articles, latitude, longitude, geoPrecision, endingDate = getArgs(request, [
        'token',
        'articles',
        'latitude',
        'longitude',
        'geoPrecision',
        'endingDate'
    ])
    latitude, longitude, geoPrecision = (float(f) for f in (latitude, longitude, geoPrecision))

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        fridge = session.query( Fridge ).filter(Fridge.user == user).first()
        if not fridge: 
            fridge = Fridge(user)
            session.add(fridge)

        donation = Donation(user, latitude, longitude, geoPrecision, endingDate)

        for value in articles:
            idArticle = value['id']
            article = session.query( Article ).filter(Article.id == idArticle).first()
            if not article: 
                message = "The article {} is unknow".format(idArticle)
                raise EmptyException(message, message, request)

            if article.idFridge != fridge.id:
                message = "The article {} is not in your fridge".format(idArticle)
                raise DonationException(message, message, request)

            if article.donation is not None:
                message = "The article {} is already in donation".format(idArticle)
                raise DonationException(message, message, request)

            article.donation = donation

        session.add(donation)
        session.commit()

        data = {'isPosted':True}

    return data