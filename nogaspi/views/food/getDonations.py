from models.objectDB import Article, Donation
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException
from facades.registerUtils import getUserFromToken
from facades.scanUtils import getArticleFromWeb


def f(request):

    token = request.args.get('token')

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        donations = session.query( Donation )

        data = {'donations': [d.toJson() for d in donations]}

    return data