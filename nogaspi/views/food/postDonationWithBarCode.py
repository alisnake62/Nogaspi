from models.objectDB import Article, Donation
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.utils.scanUtils import getArticleFromWeb


def postDonationWithBarCode(request):

    token = request.json['token']
    barcode = request.json['barcode']
    expirationDate = request.json['expirationDate']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    geoPrecision = request.json['geoPrecision']

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        article = session.query( Article ).filter(Article.barcode == barcode).first()

        if not article: 
            article = getArticleFromWeb(barcode, user, request, session)
            article.majInfoLastScan(user)
        session.add(article)
        donation = Donation(article, user, expirationDate, latitude, longitude, geoPrecision)
        session.add(donation)
        session.commit()

        data = {'isPosted':True}

    return data