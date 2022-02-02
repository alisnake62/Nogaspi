from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs
import json

def getRegularPath(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy() as session:

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