from models.objectDB import Product, Donation, Article, Fridge
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import getArgs, DonationException
from facades.utils.registerUtils import getUserFromToken
from facades.utils.scanUtils import getProductFromBarcode
from facades.utils.donationUtils import sendFireBaseNotificationsOneNewNearDonation
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

        if datetime.datetime.fromisoformat(endingDate) < datetime.datetime.now():
            message = "The given endingDate is not valid"
            raise DonationException(message, message, request)
        
        for article in articles:
            if datetime.datetime.fromisoformat(article['expirationDate']) < datetime.datetime.now() - datetime.timedelta(days=EXPIRATION_DATE_TOLERANCE_IN_DAY):
                message = "One article is expired"
                raise DonationException(message, message, request)

        donation = Donation(user, latitude, longitude, geoPrecision, endingDate)

        for article in articles:
            barcode = article['barcode']
            expirationDate = article['expirationDate']
            
            product = getProductFromBarcode(barcode, user, request, session)

            article = Article(product, donation, expirationDate, fridge)
            session.add(article)

        session.add(donation)
        session.commit()

        sendFireBaseNotificationsOneNewNearDonation(session, donation)

        data = {'isPosted':True, 'newDonationId': donation.id}

    return data