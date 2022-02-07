from models.objectDB import Allergen
from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs

def getAllergens(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        allergens = session.query( Allergen ).all()

        data = {'allergens': [a.toJson() for a in allergens]}

    return data