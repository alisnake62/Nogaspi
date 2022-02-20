### newMessage
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

### newConversation
def newConversationNotif(userFrom, conversation, messageBody):  
    return {
        'title':f"{userFrom.pseudo} veut vous parler",
        'body': f"Donation {conversation.donation.id}: {messageBody}",
        'data': {
            "event": "InitiateConversation",
            "userFrom": userFrom.pseudo,
            "idDonation": str(conversation.donation.id),
            "idConversation": str(conversation.id),
            "body": messageBody
        },
        'imageURL': None
    }
def newConversation(userFrom, userTo, conversation, messageBody):
    notif = newConversationNotif(userFrom, conversation, messageBody)
    userTo.sendFireBaseNotification(notif['title'], notif['body'], notif['data'], notif['imageURL'])

### likeDonation
def likeDonationNotif(userFrom, donation):  
    return {
        'title':f"Donation {donation.id}",
        'body': f"{userFrom.pseudo} aime votre donation",
        'data': None,
        'imageURL': None
    }
def likeDonation(userFrom, userTo, donation):
    notif = likeDonationNotif(userFrom, donation)
    userTo.sendFireBaseNotification(notif['title'], notif['body'], notif['data'], notif['imageURL'])

        