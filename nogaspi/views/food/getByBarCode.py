from models.objectDB import Article
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException
from facades.registerUtils import getUserFromToken
from facades.scanUtils import getArticleFromWeb



def f(request):

    token = request.json['token']
    barcode = request.json['barcode']

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        

        article = session.query( Article ).filter(Article.barcode == barcode).first()

        if not article: article = getArticleFromWeb(barcode, user, request)

        article.majInfoLastScan(user)
        
        data = {
            'opinion': article.opinion,
            'name': article.name,
            'brand': article.brand,
            'quantity': article.quantity,
            'barcode': article.barcode,
            'image_url': article.image_url
        }

        session.commit()
    return data