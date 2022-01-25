from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from models.objectDB import User
import json

def f(request):

    token = request.json['token']
    fireBaseToken = request.json['fireBaseToken']

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