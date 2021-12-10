from models.objectDB import Allergen
from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken


def f(request):

    token = request.args.get('token')

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        allergens = session.query( Allergen )

        data = {'allergens': [a.toJson() for a in allergens]}
    return data