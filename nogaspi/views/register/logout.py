from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken

def f(request):

    token = request.json['token']

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.killToken()
        session.commit()

        data = {'logout':True}

    return data