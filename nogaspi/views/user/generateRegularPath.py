from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import CoordException, getArgs
import json
from facades.utils.coordUtils import getPathPoints, isEquals

def generateRegularPath(request):

    token, latitudeStart, longitudeStart, latitudeEnd, longitudeEnd, pathType = getArgs(request, [
        'token',
        'latitudeStart',
        'longitudeStart',
        'latitudeEnd',
        'longitudeEnd',
        'pathType'
    ])
    latitudeStart, longitudeStart, latitudeEnd, longitudeEnd = (float(f) for f in (latitudeStart, longitudeStart, latitudeEnd, longitudeEnd))

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        if (latitudeStart, longitudeStart) == (latitudeEnd, longitudeEnd):
            message = "The coords must be different"
            raise CoordException(message, message, request)

        if (
            not isEquals(latitudeStart, longitudeStart, user.regularPathLatitudeStart, user.regularPathLongitudeStart) or
            not isEquals(latitudeEnd, longitudeEnd, user.regularPathLatitudeEnd, user.regularPathLongitudeEnd) or
            pathType != user.lastPathType
        ):
            pathPoints = getPathPoints(request, latitudeStart, longitudeStart, latitudeEnd, longitudeEnd, pathType)
            
            user.regularPathLatitudeStart = latitudeStart
            user.regularPathLongitudeStart = longitudeStart
            user.regularPathLatitudeEnd = latitudeEnd
            user.regularPathLongitudeEnd = longitudeEnd
            user.regularPathPoints = None if pathPoints is None else json.dumps(pathPoints)
            user.lastPathType = pathType

            session.commit()

        else:
            pathPoints = None if user.regularPathPoints is None else user.regularPath(False)

    regularPath = {
        'latitudeStart': latitudeStart,
        'longitudeStart': longitudeStart,
        'latitudeEnd': latitudeEnd,
        'longitudeEnd': longitudeEnd,
        'pathType': pathType,
        'pathPoints': pathPoints,
    }

    data = {'isPosted':True, 'regularPath': regularPath}

    return data