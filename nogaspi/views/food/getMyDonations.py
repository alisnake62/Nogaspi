from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken

def f(request):

    token = request.args.get('token')
    withArchived = True if request.args.get('withArchived') == "1" else False
    withExpired = True if request.args.get('withExpired') == "1" else False

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donations = user.donations

        if not withArchived:
            donations = [d for d in donations if not d.isArchived()]
        if not withExpired:
            donations = [d for d in donations if not d.isExpired()]

        data = {'Donations': [d.toJson(user) for d in donations]}
    return data