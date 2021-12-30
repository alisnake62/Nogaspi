from models.objectDB import Product, Donation, Article, Fridge
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException
from facades.registerUtils import getUserFromToken
from facades.scanUtils import getProductFromWeb
from facades.coordUtils import checkCoordRaiseException


def f(request):

    token = request.json['token']
    articles = request.json['articles']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    geoPrecision = request.json['geoPrecision']
    endingDate = request.json['endingDate']

    checkCoordRaiseException((latitude, longitude), request)

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        fridge = session.query( Fridge ).filter(Fridge.user == user).first()
        if not fridge: 
            fridge = Fridge(user)
            session.add(fridge)

        donation = Donation(user, latitude, longitude, geoPrecision, endingDate)

        for article in articles:
            barcode = article['barcode']
            expirationDate = article['expirationDate']
            product = session.query( Product ).filter(Product.barcode == barcode).first()

            if not product: 
                product = getProductFromWeb(barcode, user, request, session)
                product.majInfoLastScan(user)
                session.add(product)

            article = Article(product, donation, expirationDate, fridge)
            session.add(article)

        session.add(donation)
        session.commit()

        data = {'isPosted':True}

    return data