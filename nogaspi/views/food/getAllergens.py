from models.objectDB import Allergen, Product
from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs

def f(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        allergens = session.query( Allergen )

        data = {'allergens': [a.toJson() for a in allergens]}

    return data