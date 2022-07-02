from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs, getFiles, FileException
from werkzeug.utils import secure_filename
import os
import traceback

def postProfilePicture(request):

    token = getArgs(request, ['token'])
    profilePicture = getFiles(request, ['profilePicture'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        if user.profilePicture is not None and os.path.isfile(f"{os.environ['DIRECTORY_PROJECT']}assets/images/users/{user.profilePicture}"):
            os.remove(f"{os.environ['DIRECTORY_PROJECT']}assets/images/users/{user.profilePicture}")

        try:
            extension = secure_filename(profilePicture.filename).split('.')[-1]
            filename = f"{user.pseudo}.{extension}"
            profilePicture.save(f"{os.environ['DIRECTORY_PROJECT']}assets/images/users/{filename}")
        except Exception:
            raise FileException("Problem to save the file", traceback.format_exc(), request)

        user.profilePicture = filename
        session.commit()

        data = {'isPosted':True}

    return data