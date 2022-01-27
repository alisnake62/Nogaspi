from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken

def f(request):

    token = request.args.get('token')
    withArchived = request.args.get('withArchived') == "1"
    withExpired = request.args.get('withExpired') == "1"

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        donations = user.donations

        if not withArchived:
            donations = [d for d in donations if not d.isArchived()]
        if not withExpired:
            donations = [d for d in donations if not d.isExpired()]

        data = {'donations': [d.toJson(user) for d in donations]}
    return data