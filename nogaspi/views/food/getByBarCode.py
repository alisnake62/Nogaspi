from models.objectDB import Article, Allergen
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException
from facades.registerUtils import getUserFromToken
from facades.scanUtils import getArticleFromWeb

import json


def f(request):

    token = request.json['token']
    barcode = request.json['barcode']

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        article = session.query( Article ).filter(Article.barcode == barcode).first()

        if not article: article = getArticleFromWeb(barcode, user, request)

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
            #'allergen' : json.loads(article.allergen.nameEN)
        }

        
    return data