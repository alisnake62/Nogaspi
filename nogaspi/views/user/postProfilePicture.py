from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from models.objectDB import User
from facades.apiConfig import getArgs, getFiles

def postProfilePicture(request):

    token = getArgs(request, ['token'])
    profilePicture = getFiles(request, ['profilePicture'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        data = {'isPosted':True}

    return data