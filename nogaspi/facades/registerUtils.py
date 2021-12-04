import datetime

from models.objectDB import User
from apiConfig import TokenException

def getUserFromToken(token, session, request):
    user = session.query( User ).filter(User.token == token).first()

    if not user:
        raise TokenException("Token incorrect", request)
    elif user.token_expiration < datetime.datetime.now():
        raise TokenException("Token expired", request)

    return user

def majTokenValidity(user, session, request):
    pass