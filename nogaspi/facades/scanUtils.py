import requests as req
import traceback
from models.objectDB import Article, Allergen
from apiConfig import OpenFoodException

import json

class ArticleHTTP:
    name = None
    quantity = None
    brand = None
    image_url = None
    ingredients = None
    nutrimentData = {}
    nutriscoreData = {}
    allergens = []

    def __init__(self, articleHTTP):
        self.articleHTTP = articleHTTP
        self.name = self.getProductInfo('product_name')
        self.quantity = self.getProductInfo('quantity')
        self.brand = self.getProductInfo('brands')
        self.image_url = self.getProductInfo('image_url')
        self.ingredients = self.getProductInfo('ingredients_text_fr')
        if self.getProductInfo('nutriments') is not None:
            self.nutrimentData = self.getProductInfo('nutriments')
        self.nutrimentData = json.dumps(self.nutrimentData)
        if self.getProductInfo('nutriscore_data') is not None:
            self.nutriscoreData = self.getProductInfo('nutriscore_data')
        self.nutriscoreData = json.dumps(self.nutriscoreData)
        if self.getProductInfo('allergens_hierarchy') is not None:
            self.allergens = self.getProductInfo('allergens_hierarchy')

    def getProductInfo(self, info):
        if info in self.articleHTTP: return self.articleHTTP[info]
        else: return None


def getArticleFromWeb(barcode, user, request, session):
    
    url = "https://world.openfoodfacts.org/api/v0/product/{}.json".format(barcode)

    try:
        articleHTTP = req.get(url).json()
    except Exception:
        raise OpenFoodException("Problem to access at OpenFood web Service", traceback.format_exc(), request)

    if articleHTTP['status'] == 0: 
        message = "This barcode is unknown in the WebService"
        raise OpenFoodException(message, message, request)
    
    articleHTTP = ArticleHTTP(articleHTTP['product'])

    article = Article(
        user,
        name = articleHTTP.name,
        quantity = articleHTTP.quantity,
        barcode=barcode, 
        brand = articleHTTP.brand,
        image_url=articleHTTP.image_url,
        ingredients=articleHTTP.ingredients,
        nutrimentData = articleHTTP.nutrimentData,
        nutriscoreData = articleHTTP.nutriscoreData
    )
    article.allergens = majAllergenInDB(articleHTTP.allergens, session)

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