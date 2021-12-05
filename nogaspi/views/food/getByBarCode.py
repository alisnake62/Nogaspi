from models.objectDB import User, Article
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException
from facades.registerUtils import getUserFromToken, majTokenValidity

def f(request):

    token = request.json['token']
    barcode = request.json['barcode']

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        majTokenValidity(token, session, request)

        article = session.query( Article ).filter(Article.barcode == barcode).first()

        if not article:
            message = "No article with this barcode"
            raise EmptyException(message, message, request)

        data = {
            'opinion': article.opinion,
            'name': article.name,
            'brand': article.brand,
            'quantity': article.quantity,
            'barcode': article.barcode,
            'image_url': article.image_url
        }

        return data