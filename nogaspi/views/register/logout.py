from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs

def logout(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.killToken()
        session.commit()

        data = {'logout':True}

    return data