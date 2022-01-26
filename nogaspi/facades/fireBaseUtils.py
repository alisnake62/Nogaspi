import os
import traceback
from apiConfig import logging
import firebase_admin
from firebase_admin import messaging, credentials, initialize_app

def sendNotification(idUserTo, fireBaseToken, title, body, ):

    initAppOnFireBase()

    try:
        message = messaging.Message(
            notification=messaging.Notification(title, body, image=f"https://monappli.ovh:5556/tools/getProfilePicture?idUser={idUserTo}"),
            token=fireBaseToken,
        )
        messaging.send(message)
    except Exception:
        logging.error(traceback.format_exc())
    

def initAppOnFireBase():

    cred = credentials.Certificate(os.environ['FIREBASE_SERVICE_ACCOUNT'])
    try:
        if not firebase_admin._apps:
            initialize_app(cred)
    except Exception:
        logging.error(traceback.format_exc())
