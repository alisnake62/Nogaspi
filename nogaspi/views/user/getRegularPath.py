from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs

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
            'pathType': user.lastPathType,
            'pathPoints': None if user.regularPathPoints is None else user.regularPath(False)
        }

        data = {'regularPath': regularPath}
    return data