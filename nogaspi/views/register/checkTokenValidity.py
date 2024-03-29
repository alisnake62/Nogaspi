import datetime
from models.objectDB import User
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import getArgs

def checkTokenValidity(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy() as session:

        user = session.query( User ).filter(User.token == token).first()

        if not user:
            return {'validity': False, 'user' : 'Unknown', 'token_expiration': 'Unknown'}
        elif user.token_expiration < datetime.datetime.now():
            return {'validity': False, 'user' : user.mail, 'token_expiration': user.token_expiration}
        else:
            user.majTokenValidity()
            return {'validity': True, 'user' : user.mail, 'token_expiration': user.token_expiration}