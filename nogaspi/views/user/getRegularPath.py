from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken

def f(request):

    token = request.args.get('token')

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
       
        regularPath = {
            'latitudeStart': user.regularPathLatitudeStart,
            'longitudeStart': user.regularPathLongitudeStart,
            'latitudeEnd': user.regularPathLatitudeEnd,
            'longitudeEnd': user.regularPathLongitudeEnd
        }

        data = {'regularPath': regularPath}
    return data