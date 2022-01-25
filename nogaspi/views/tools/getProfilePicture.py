from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from models.objectDB import User
import json
import os

def f(request):

    idUser = int(request.args.get('idUser'))

    with EngineSQLAlchemy(request) as session:

        user = session.query(User).filter(User.id == idUser).first()
        
        if not user:
            picture = "emptyProfile.jpg"
        elif user.profilePicture is None:
            picture = "emptyProfile.jpg"
        elif not os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/../../../../images/users/{user.profilePicture}"):
            picture = "emptyProfile.jpg"
        else:
            picture = user.profilePicture

        data = {'picturePath': f"../../images/users/{picture}"}
    return data