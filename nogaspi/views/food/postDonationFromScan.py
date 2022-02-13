from models.objectDB import Product, Donation, Article, Fridge
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import getArgs, DonationException
from facades.utils.registerUtils import getUserFromToken
from facades.utils.scanUtils import getProductFromWeb
from facades.const import EXPIRATION_DATE_TOLERANCE_IN_DAY
import datetime


def postDonationFromScan(request):

    token, articles, latitude, longitude, geoPrecision, endingDate = getArgs(request, [
        'token',
        'articles',
        'latitude',
        'longitude',
        'geoPrecision',
        'endingDate'
    ])
    latitude, longitude, geoPrecision = (float(f) for f in (latitude, longitude, geoPrecision))

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        fridge = session.query( Fridge ).filter(Fridge.user == user).first()
        if not fridge: 
            fridge = Fridge(user)
            session.add(fridge)

        for article in articles:
            if datetime.datetime.fromisoformat(article['expirationDate']) < datetime.datetime.now() - datetime.timedelta(days=EXPIRATION_DATE_TOLERANCE_IN_DAY):
                message = "One article is expired"
                raise DonationException(message, message, request)

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