from models.objectDB import User
from facades.utils.mailUtils import sendConfirmationCode
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import RegisterException
from facades.apiConfig import getArgs

def createUser(request):

    mail, password, pseudo = getArgs(request, ['mail', 'password', 'pseudo'])

    with EngineSQLAlchemy() as session:

        user = session.query( User ).filter(User.mail == mail).first()

        if user:
            if user.isConfirmate:
                message = f"The user {mail} already exist"
                raise RegisterException(message, message, request)
            user.pseudo = pseudo
            user.password = password
        else:
            samePseudoUsers = session.query( User ).filter(User.pseudo == pseudo).all()

            for samePseudoUser in samePseudoUsers:
                if samePseudoUser.isConfirmate:
                    message = f"The pseudo {pseudo} is already used"
                    raise RegisterException(message, message, request)
            
            user = User(mail, password, pseudo)
            session.add(user)

        user.generateConfirmationCode()
        session.commit()

        from threading import Thread

        sendConfirmationCode(mail, pseudo, user.confirmationCode)

    return {'userCreateConfirmationCodeAsk': True}