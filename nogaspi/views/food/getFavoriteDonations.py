from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from apiConfig import getArgs

def f(request):

    token, = getArgs(request, ['token'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        data = {'favoriteDonations': [d.toJson(user) for d in user.favoriteDonations if d.isValide()]}
    return data