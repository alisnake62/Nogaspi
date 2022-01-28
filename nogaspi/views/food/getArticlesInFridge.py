
from models.objectDB import Fridge
from dbEngine import EngineSQLAlchemy
from apiConfig import getArgs
from facades.registerUtils import getUserFromToken


def f(request):

    token = getArgs(request, ['token'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        
        fridge = session.query( Fridge ).filter(Fridge.user == user).first()
        if not fridge: 
            fridge = Fridge(user)
            session.add(fridge)

        data = fridge.toJson()
    return data