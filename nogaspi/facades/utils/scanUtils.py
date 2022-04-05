import requests as req
import traceback
import datetime
from models.objectDB import Product, Allergen
from facades.apiConfig import OpenFoodException
from facades.const import PRODUCT_DATA_VALIDITY

import json

class ProductHTTP:
    name = None
    quantity = None
    brand = None
    image_url = None
    ingredients = None
    nutrimentData = {}
    nutriscoreData = {}
    allergens = []

    def __init__(self, productHTTP):
        self.productHTTP = productHTTP
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
        return self.productHTTP[info] if info in self.productHTTP else None

def getProductFromBarcode(barcode, user, request, session):
    product = session.query( Product ).filter(Product.barcode == barcode).first()

    if not product or product.lastScanDate < datetime.datetime.now() - datetime.timedelta(days=PRODUCT_DATA_VALIDITY):
        product = getProductFromWeb(barcode, user, request, session)
        product.majInfoLastScan(user)
        session.commit()
    
    return product


def getProductFromWeb(barcode, user, request, session):
    
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    try:
        productHTTP = req.get(url).json()
    except Exception:
        raise OpenFoodException("Problem to access at OpenFood web Service", traceback.format_exc(), request)

    if productHTTP['status'] == 0: 
        message = "This barcode is unknown in the WebService"
        raise OpenFoodException(message, message, request)
    
    productHTTP = ProductHTTP(productHTTP['product'])

    product = Product(
        user,
        datetime.datetime.now(),
        name = productHTTP.name,
        quantity = productHTTP.quantity,
        barcode=barcode, 
        brand = productHTTP.brand,
        image_url=productHTTP.image_url,
        ingredients=productHTTP.ingredients,
        nutrimentData = productHTTP.nutrimentData,
        nutriscoreData = productHTTP.nutriscoreData
    )
    product.allergens = majAllergenInDB(productHTTP.allergens, session)

    return product

def majAllergenInDB(allergensHTTP, session):
    allergens = []
    for enAllergenString in allergensHTTP:
        enAllergenString = enAllergenString.split(':')[-1].capitalize()
        allergen = session.query( Allergen ).filter(Allergen.nameEN == enAllergenString).first()
        if allergen is None:
            allergen = Allergen(enAllergenString)
        allergens.append(allergen)
    return allergens