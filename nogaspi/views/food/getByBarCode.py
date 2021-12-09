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

        data = {
            'opinion': article.opinion,
            'name': article.name,
            'brand': article.brand,
            'quantity': article.quantity,
            'barcode': article.barcode,
            'image_url': article.image_url,
            'ingredient' : article.ingredients,
            'nutrimentsData' : json.loads(article.nutrimentData),
            'nutriscoreData' : json.loads(article.nutriscoreData),
            'allergens': [a.nameEN if a.nameFR is None else a.nameFR for a in article.allergens ]
        }

    return data