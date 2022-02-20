def newMessageNotif(userFrom, conversation, messageBody):  
    return {
        'title': f"Message reçu de {userFrom.pseudo}",
        'body': f"Donation {conversation.donation.id}: {messageBody}",
        'data': {
            "event": "NewMessage",
            "userFrom": userFrom.pseudo,
            "idDonation": str(conversation.donation.id),
            "idConversation": str(conversation.id),
            "body": messageBody
        },
        'imageURL': None
    }
def newMessage(userFrom, userTo, conversation, messageBody):
    notif = newMessageNotif(userFrom, conversation, messageBody)
    userTo.sendFireBaseNotification(notif['title'], notif['body'], notif['data'], notif['imageURL'])
