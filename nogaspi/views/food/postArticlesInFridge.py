from models.objectDB import Product, Article, Fridge
from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.utils.scanUtils import getProductFromWeb
from facades.apiConfig import getArgs, FridgeException
from facades.const import EXPIRATION_DATE_TOLERANCE_IN_DAY

import datetime


def postArticlesInFridge(request):
    
    token, articles = getArgs(request, ['token', 'articles'])

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
                raise FridgeException(message, message, request)

        for article in articles:
            barcode = article['barcode']
            expirationDate = article['expirationDate']
            product = session.query( Product ).filter(Product.barcode == barcode).first()

            if not product: 
                product = getProductFromWeb(barcode, user, request, session)
                product.majInfoLastScan(user)
                session.add(product)

            article = Article(product, None, expirationDate, fridge)
            session.add(article)

        session.commit()

        data = {'isPosted':True}

    return data