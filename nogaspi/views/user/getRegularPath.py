from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from apiConfig import getArgs
import json

def f(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
       
        regularPath = {
            'latitudeStart': user.regularPathLatitudeStart,
            'longitudeStart': user.regularPathLongitudeStart,
            'latitudeEnd': user.regularPathLatitudeEnd,
            'longitudeEnd': user.regularPathLongitudeEnd,
            'pathPoints': None if user.regularPathPoints is None else json.loads(user.regularPathPoints)
        }

        data = {'regularPath': regularPath}
    return data