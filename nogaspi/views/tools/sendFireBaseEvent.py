from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs

def sendFireBaseEvent(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        user.sendFireBaseEvent("charlyLulu", {'data1': str(3), 'data2': 'test2'})
        
    return {'data': 'test'}