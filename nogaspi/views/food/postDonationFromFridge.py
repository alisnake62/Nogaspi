from models.objectDB import Product, Donation, Article, Fridge
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException, DonationException
from facades.registerUtils import getUserFromToken
from facades.scanUtils import getProductFromWeb


def f(request):

    token = request.json['token']
    articles = request.json['articles']
    latitude = float(request.json['latitude'])
    longitude = float(request.json['longitude'])
    geoPrecision = float(request.json['geoPrecision'])
    endingDate = request.json['endingDate']

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