import requests as req
import traceback
from models.objectDB import Article, Allergen
from apiConfig import OpenFoodException

import json

def getArticleFromWeb(barcode, user, request, session):
    
    url = "https://world.openfoodfacts.org/api/v0/product/{}.json".format(barcode)

    try:
        articleHTTP = req.get(url).json()
    except Exception:
        raise OpenFoodException("Problem to access at OpenFood web Service", traceback.format_exc(), request)

    if articleHTTP['status'] == 0: raise OpenFoodException("This barcode is unknown in the WebService", traceback.format_exc(), request)

    articleHTTP = articleHTTP['product']

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
    article.allergens = majAllergenInDB(articleHTTP['allergens_hierarchy'], session)

    return article




def majAllergenInDB(allergensHTTP, session):
    allergens = []
    for enAllergenString in allergensHTTP:
        enAllergenString = enAllergenString.split(':')[-1].capitalize()
        allergen = session.query( Allergen ).filter(Allergen.nameEN == enAllergenString).first()
        if allergen is None:
            allergen = Allergen(enAllergenString)
        allergens.append(allergen)
    return allergens