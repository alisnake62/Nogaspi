from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from models.objectDB import User
from facades.apiConfig import getArgs

def f(request):

    token, fireBaseToken = getArgs(request, ['token', 'fireBaseToken'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        #clear fireBase Token in DB
        usersToClear = session.query(User).filter(User.fireBaseToken == fireBaseToken).all()
        for userToClear in usersToClear:
            userToClear.fireBaseToken = None

        user.fireBaseToken = fireBaseToken

        session.commit()

        data = {'isPosted':True}

    return data