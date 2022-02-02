
from models.objectDB import Fridge
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import getArgs
from facades.utils.registerUtils import getUserFromToken


def getArticlesInFridge(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        
        fridge = session.query( Fridge ).filter(Fridge.user == user).first()
        if not fridge: 
            fridge = Fridge(user)
            session.add(fridge)

        data = fridge.toJson()
    return data