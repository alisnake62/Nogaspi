from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from apiConfig import CoordException
import json

def f(request):

    token = request.json['token']
    latitudeStart = float(request.json['latitudeStart'])
    longitudeStart = float(request.json['longitudeStart'])
    latitudeEnd = float(request.json['latitudeEnd'])
    longitudeEnd = float(request.json['longitudeEnd'])
    pathPoints = request.json['pathPoints']

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