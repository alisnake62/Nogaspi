from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs

def getMyDonations(request):

    token, withArchived, withExpired = getArgs(request, ['token', 'withArchived', 'withExpired'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donations = user.donations

        if withArchived == "0":
            donations = [d for d in donations if not d.isArchived()]
        if withExpired == "0":
            donations = [d for d in donations if not d.isExpired()]

        data = {'donations': [d.toJson(user) for d in donations]}
    return data