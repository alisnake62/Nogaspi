from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from models.objectDB import User
from facades.apiConfig import getArgs
import os

def getProfilePicture(request):

    idUser = getArgs(request, ['idUser'])

    with EngineSQLAlchemy() as session:

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