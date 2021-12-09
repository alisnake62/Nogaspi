from models.objectDB import Article, Allergen
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException
from facades.registerUtils import getUserFromToken
from facades.scanUtils import getArticleFromWeb

import json


def f(request):

    token = request.args.get('token')
    barcode = request.args.get('barcode')

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        article = session.query( Article ).filter(Article.barcode == barcode).first()

        if not article: article = getArticleFromWeb(barcode, user, request, session)

        article.majInfoLastScan(user)
        session.commit()

        data = article.toJson()

    return data