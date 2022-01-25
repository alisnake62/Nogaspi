import os
import traceback
from apiConfig import logging
import firebase_admin
from firebase_admin import messaging, credentials, initialize_app

def sendNotification(fireBaseToken, title, body):

    initAppOnFireBase()

    try:
        message = messaging.Message(
            notification=messaging.Notification(title, body, image="https://localhost:5000/tools/getprofilePicture?token=63df50a9bdbc5ffe047fad0c26f8908cbf0fc5c9786c9144d319206ec25bfd1b"),
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
