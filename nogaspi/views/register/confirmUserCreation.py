import datetime
from models.objectDB import User
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import RegisterException
from facades.apiConfig import getArgs

def confirmUserCreation(request):

    mail, confirmationCode = getArgs(request, ['mail', 'confirmationCode'])

    with EngineSQLAlchemy() as session:

        user = session.query( User ).filter(User.mail == mail).first()

        if not user:
            message = f"The user {mail} doesn't exist"
            raise RegisterException(message, message, request)

        if user.isConfirmate:
            message = f"The user {mail} is already confirmate"
            raise RegisterException(message, message, request)

        if not user.confirmationCodeIsValide(confirmationCode):
            message = f"The confirmation code is not valid"
            raise RegisterException(message, message, request)

        user.isConfirmate = True
        session.commit()

    return {'isConfirmate': True}