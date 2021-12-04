from models.objectDB import User
from dbEngine import EngineSQLAlchemy
from apiConfig import RegisterException, TokenException

def f(request):

    mail = request.json['mail']
    password = request.json['password']

    with EngineSQLAlchemy() as session:

        try:
            user = session.query( User ).filter(User.mail == mail).first()
            if (user.password != password): raise Exception()
        except Exception as e:
            print(type(e), e)
            raise RegisterException("login / password incorrect", request)

        try:
            tokenInfo = user.generateToken()
            session.commit()
            
        except Exception as e:
            print(type(e), e)
            raise TokenException("problem to generate token", request)

    return tokenInfo