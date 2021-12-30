from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken

def f(request):

    token = request.args.get('token')

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
       
        regularPath = {
            'latitude1': user.regularPathLatitude1,
            'longitude1': user.regularPathLongitude1,
            'latitude2': user.regularPathLatitude2,
            'longitude2': user.regularPathLongitude2
        }

        data = {'regularPath': regularPath}
    return data