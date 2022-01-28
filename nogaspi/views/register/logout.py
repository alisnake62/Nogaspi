from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from apiConfig import getArgs

def f(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.killToken()
        session.commit()

        data = {'logout':True}

    return data