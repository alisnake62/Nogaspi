import datetime

from models.objectDB import User
from facades.apiConfig import TokenException

def getUserFromToken(token, session, request):
    user = session.query( User ).filter(User.token == token).first()

    if not user:
        message = "Token unknown"
        raise TokenException(message, message, request)
    elif user.token_expiration < datetime.datetime.now():
        message = "Token expired"
        raise TokenException(message, message, request)

    return user