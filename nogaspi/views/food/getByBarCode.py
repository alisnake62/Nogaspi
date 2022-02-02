from models.objectDB import Product, Allergen
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.utils.scanUtils import getProductFromWeb

import json


def getByBarCode(request):

    token, barcode = getArgs(request, ['token', 'barcode'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        product = session.query( Product ).filter(Product.barcode == barcode).first()

        if not product: product = getProductFromWeb(barcode, user, request, session)

        product.majInfoLastScan(user)
        session.commit()

        data = product.toJson()

    return data