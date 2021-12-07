import requests as req
import traceback
from models.objectDB import Article, Allergen
from apiConfig import OpenFoodException

import json

def getArticleFromWeb(barcode, user, request):
    
    url = "https://world.openfoodfacts.org/api/v0/product/{}.json".format(barcode)

    try:
        articleHTTP = req.get(url).json()
    except Exception:
        raise OpenFoodException("Problem to access at OpenFood web Service", traceback.format_exc(), request)

    if articleHTTP['status'] == 0: raise OpenFoodException("This barcode is unknown in the WebService", traceback.format_exc(), request)

    articleHTTP = articleHTTP['product']

    # gerer la pultiplicité de l'allergen + check si ils sont pas déjà en base
    allergen = Allergen(json.dumps(articleHTTP['allergens_hierarchy']))

    article = Article(
        articleHTTP['product_name'],
        articleHTTP['quantity'],
        user.id, brand = articleHTTP['brands'],
        barcode=barcode,
        image_url=articleHTTP['image_url'],
        ingredients=articleHTTP['ingredients_text_fr'],
        nutrimentData = json.dumps(articleHTTP['nutriments']),
        nutriscoreData = json.dumps(articleHTTP['nutriscore_data']),
    )
    article.allergen = allergen

    return article, allergen