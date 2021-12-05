import requests as req
import traceback
from models.objectDB import Article
from apiConfig import OpenFoodException

def getArticleFromWeb(barcode, user, request):
    
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
        image_url=articleHTTP['image_url']
    )

    return article