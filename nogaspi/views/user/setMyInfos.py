from models.objectDB import Allergen
from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs, EmptyException

def setMyInfos(request):

    token, address, idAllergen, favoriteDistanceToSearch, favoriteGeoPrecisionToDonate = getArgs(request, [
        'token',
        'address',
        'idAllergen',
        'favoriteDistanceToSearch',
        'favoriteGeoPrecisionToDonate'
    ])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        if idAllergen is not None:
            allergen = session.query( Allergen ).filter(Allergen.id == idAllergen).first()
            if not allergen:
                message = "The allergen is not present in Database"
                raise EmptyException(message, message, request)

        user.address = address
        user.allergen = allergen if idAllergen is not None else None
        user.favoriteDistanceToSearch = favoriteDistanceToSearch
        user.favoriteGeoPrecisionToDonate = favoriteGeoPrecisionToDonate

        session.commit()


    return {'isSetted': True}