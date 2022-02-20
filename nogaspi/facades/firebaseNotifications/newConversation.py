def newConversationNotif(userFrom, conversation, messageBody):  
    return {
        'title': f"{userFrom.pseudo} veut vous parler",
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
