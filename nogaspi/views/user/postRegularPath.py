from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import CoordException, getArgs
import json

def postRegularPath(request):

    token, latitudeStart, longitudeStart, latitudeEnd, longitudeEnd, pathPoints = getArgs(request, [
        'token',
        'latitudeStart',
        'longitudeStart',
        'latitudeEnd',
        'longitudeEnd',
        'pathPoints'
    ])
    latitudeStart, longitudeStart, latitudeEnd, longitudeEnd = (float(f) for f in (latitudeStart, longitudeStart, latitudeEnd, longitudeEnd))

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        if (latitudeStart, longitudeStart) == (latitudeEnd, longitudeEnd):
            message = "The coords must be different"
            raise CoordException(message, message, request)

        user.regularPathLatitudeStart = latitudeStart
        user.regularPathLongitudeStart = longitudeStart
        user.regularPathLatitudeEnd = latitudeEnd
        user.regularPathLongitudeEnd = longitudeEnd
        user.regularPathPoints = json.dumps(pathPoints)

        session.commit()

        data = {'isPosted':True}

    return data