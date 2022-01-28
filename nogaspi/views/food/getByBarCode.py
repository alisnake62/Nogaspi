from models.objectDB import Product, Allergen
from dbEngine import EngineSQLAlchemy
from apiConfig import getArgs
from facades.registerUtils import getUserFromToken
from facades.scanUtils import getProductFromWeb

import json


def f(request):

    token, barcode = getArgs(request, ['token', 'barcode'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        product = session.query( Product ).filter(Product.barcode == barcode).first()

        if not product: product = getProductFromWeb(barcode, user, request, session)

        product.majInfoLastScan(user)
        session.commit()

        data = product.toJson()

    return data