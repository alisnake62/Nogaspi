import os
import traceback

from facades.apiConfig import logging
import firebase_admin
from firebase_admin import messaging, credentials, initialize_app
from facades.const import ANDROID_GLOBAL_ACTIVITY

def sendNotification(fireBaseToken, event, data, title, body, imageURL):

    if os.environ['LAUNCH_ENV'] == 'test': return

    if data: data['event'] = event
    else: data = {'event': event}
    
    initAppOnFireBase()
    try:
        message = messaging.Message(
            android = messaging.AndroidConfig(
                notification=messaging.AndroidNotification(title=title, body=body, image=imageURL, click_action=ANDROID_GLOBAL_ACTIVITY)
            ),
            #notification = messaging.Notification(title=title, body=body, image=imageURL),
            data = data,
            token=fireBaseToken
        )
        messaging.send(message)
    except Exception:
        logging.error(traceback.format_exc())

def sendEvent(fireBaseToken, event, data):

    if os.environ['LAUNCH_ENV'] == 'test': return

    if data: data['event'] = event
    else: data = {'event': event}

    initAppOnFireBase()
    try:
        message = messaging.Message(
            data = data,
            token = fireBaseToken
        )
        messaging.send(message)
    except Exception:
        logging.error(traceback.format_exc())

def sendNotificationMultiUser(fireBaseTokens, event, data, title, body, imageURL):

    if os.environ['LAUNCH_ENV'] == 'test': return

    if data: data['event'] = event
    else: data = {'event': event}
    
    initAppOnFireBase()
    try:
        message = messaging.MulticastMessage(
            android = messaging.AndroidConfig(
                notification=messaging.AndroidNotification(title=title, body=body, image=imageURL, click_action=ANDROID_GLOBAL_ACTIVITY)
            ),
            #notification=messaging.Notification(title=title, body=body, image=imageURL),
            data = data,
            tokens = fireBaseTokens
        )
        messaging.send_multicast(message)
    except Exception:
        logging.error(traceback.format_exc())

def initAppOnFireBase():

    cred = credentials.Certificate(f"{os.environ['DIRECTORY_ASSET']}{os.environ['FIREBASE_SERVICE_ACCOUNT']}")
    try:
        if not firebase_admin._apps:
            initialize_app(cred)
    except Exception:
        logging.error(traceback.format_exc())
