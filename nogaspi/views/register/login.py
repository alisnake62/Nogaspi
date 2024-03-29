from models.objectDB import User
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import RegisterException, TokenException
from facades.apiConfig import getArgs

import traceback

def login(request):

    mail, password = getArgs(request, ['mail', 'password'])

    with EngineSQLAlchemy() as session:

        try:
            user = session.query( User ).filter(User.mail == mail).first()
            if user.password != password: raise Exception()
            if not user.isConfirmate: raise Exception()
        except Exception:
            raise RegisterException("login / password incorrect", traceback.format_exc(), request)

        try:
            tokenInfo = user.generateToken()
            session.commit()
            
        except Exception:
            raise TokenException("problem to generate token", traceback.format_exc(), request)

    return tokenInfo