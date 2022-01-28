from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from apiConfig import getArgs

def f(request):

    token, withArchived, withExpired = getArgs(request, ['token', 'withArchived', 'withExpired'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donations = user.donations

        if withArchived == "0":
            donations = [d for d in donations if not d.isArchived()]
        if withExpired == "0":
            donations = [d for d in donations if not d.isExpired()]

        data = {'donations': [d.toJson(user) for d in donations]}
    return data