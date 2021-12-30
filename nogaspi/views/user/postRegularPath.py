from Nogaspi.nogaspi.facades.coordUtils import checkCoordRaiseException
from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from facades.coordUtils import checkCoordRaiseException
from apiConfig import CoordException

def f(request):

    token = request.json['token']
    latitude1 = float(request.json['latitude1'])
    longitude1 = float(request.json['longitude1'])
    latitude2 = float(request.json['latitude2'])
    longitude2 = float(request.json['longitude2'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        checkCoordRaiseException((latitude1, longitude1), request)
        checkCoordRaiseException((latitude2, longitude2), request)
        if (latitude1, longitude1) ==(latitude2, longitude2):
            message = "The coords must be different"
            raise CoordException(message, message, request)

        user.regularPathLatitude1 = latitude1
        user.regularPathLongitude1 = longitude1
        user.regularPathLatitude2 = latitude2
        user.regularPathLongitude2 = longitude2

        session.commit()

        data = {'isPosted':True}

    return data