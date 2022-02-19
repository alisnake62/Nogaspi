import os
import traceback
from facades.apiConfig import logging
import firebase_admin
from firebase_admin import messaging, credentials, initialize_app

# processing this if it's not ok
""" 
    action_process = Process(target=do_actions)
 
    # We start the process and we block for 5 seconds.
    action_process.start()
    action_process.join(timeout=5)
 
    # We terminate the process.
    action_process.terminate()
    print("Hey there! I timed out! You can do things after me!")
"""

def sendNotification(fireBaseToken, title, body, imageURL = None):

    initAppOnFireBase()
    try:
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body, image=imageURL),
            token=fireBaseToken,
        )
        messaging.send(message)
    except Exception:
        logging.error(traceback.format_exc())
    

def initAppOnFireBase():

    cred = credentials.Certificate(f"{os.environ['DIRECTORY_ASSET']}{os.environ['FIREBASE_SERVICE_ACCOUNT']}")
    try:
        if not firebase_admin._apps:
            initialize_app(cred)
    except Exception:
        logging.error(traceback.format_exc())
