def newMessageMessage(userFrom, conversation, messageBody):  
    return {
        'title': f"Message reçu de {userFrom.pseudo}",
        'body': f"Donation {conversation.donation.id}: {messageBody}",
        'data': {
            "userFrom": userFrom.pseudo,
            "idDonation": str(conversation.donation.id),
            "idConversation": str(conversation.id)
        },
        'imageURL': None
    }
def newMessage(userFrom, userTo, conversation, messageBody):
    message = newMessageMessage(userFrom, conversation, messageBody)
    userTo.sendFireBaseNotification('newMessage', message['title'], message['body'], message['imageURL'], message['data'])
