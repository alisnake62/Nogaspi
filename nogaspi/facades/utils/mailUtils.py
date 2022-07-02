import os
import traceback
from facades.apiConfig import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendConfirmationCode(mailTo, pseudo, code):
    
    if os.environ['LAUNCH_ENV'] == 'test': return

    mailFrom = os.environ['MAIL_SENDER']
    password = os.environ['MAIL_SENDER_PASSWORD']

    mail_subject = "NoGaspi - Inscription"

    try:
        templateMailPath = f"{os.environ['DIRECTORY_PROJECT']}Nogaspi/nogaspi/models/templates/confirmationCode.html"
        with open(templateMailPath, 'r') as templateMailFile:
            templateMail = templateMailFile.read()

        mail_body = templateMail.replace("--VAR_PSEUDO--", pseudo).replace("--VAR_CODE--", code)

        mimemsg = MIMEMultipart()
        mimemsg['From']=mailFrom
        mimemsg['To']=mailTo
        mimemsg['Subject']=mail_subject
        mimemsg.attach(MIMEText(mail_body, 'html'))
        connection = smtplib.SMTP(host='smtp.office365.com', port=587)
        connection.starttls()
        connection.login(mailFrom,password)
        connection.send_message(mimemsg)
        connection.quit()
    except Exception:
        logging.error(traceback.format_exc())

    
