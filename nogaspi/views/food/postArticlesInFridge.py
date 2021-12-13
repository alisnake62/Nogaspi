from models.objectDB import Product, Article, Fridge
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException
from facades.registerUtils import getUserFromToken
from facades.scanUtils import getProductFromWeb


def f(request):

    token = request.json['token']
    articles = request.json['articles']

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        fridge = session.query( Fridge ).filter(Fridge.user == user).first()
        if not fridge: 
            fridge = Fridge(user)
            session.add(fridge)

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