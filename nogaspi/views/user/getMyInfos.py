from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs
import json

def getMyInfos(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
       
        data = user.toJson(userRequester=user)

    return data