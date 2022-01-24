from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
import json

def f(request):

    token = request.json['token']
    fireBaseToken = request.json['fireBaseToken']

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        user.fireBaseToken = fireBaseToken

        session.commit()

        data = {'isPosted':True}

    return data