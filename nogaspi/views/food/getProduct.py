from models.objectDB import Product
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import getArgs
from facades.utils.registerUtils import getUserFromToken
from facades.utils.scanUtils import getProductFromBarcode

def getProduct(request):

    token, barcode = getArgs(request, ['token', 'barcode'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        product = getProductFromBarcode(barcode, user, request, session)

        data = product.toJson()

    return data