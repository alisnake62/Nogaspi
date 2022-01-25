from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
import json
import os

def f(request):

    token = request.args.get('token')

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        data = {'picturePath': f"../../images/users/{user.profilePicture}"}
    return data