import datetime
from facades.apiConfig import getArgs
from models.objectDB import User
from dbEngine import EngineSQLAlchemy

def checkTokenValidity(request):

    token = getArgs(request, ['token'])
    checkTokenValidityTest(token, request)

def checkTokenValidityTest(token):

    with EngineSQLAlchemy() as session:

        user = session.query( User ).filter(User.token == token).first()

        if not user:
            return {'validity': False, 'user' : 'Unknown', 'token_expiration': 'Unknown'}
        elif user.token_expiration < datetime.datetime.now():
            return {'validity': False, 'user' : user.mail, 'token_expiration': user.token_expiration}
        else:
            user.majTokenValidity()
            return {'validity': True, 'user' : user.mail, 'token_expiration': user.token_expiration}