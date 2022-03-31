from facades.const import MAX_LETTER_COUNT_ON_NOTIFICATION

def body(donation, message):

    body = message.toStringToNotification(donation)


    bodySize = len(body)

    if bodySize > MAX_LETTER_COUNT_ON_NOTIFICATION: 
        body = body[:MAX_LETTER_COUNT_ON_NOTIFICATION] + "..."

    return body

def newMessageMessage(userFrom, conversation, message):  
    return {
        'title': f"Message reçu de {userFrom.pseudo}",
        'body': f"Donation {conversation.donation.id}: {message}",
        'data': {
            "userFrom": userFrom.pseudo,
            "idDonation": str(conversation.donation.id),
            "idConversation": str(conversation.id)
        },
        'imageURL': None
    }
def newMessage(userFrom, userTo, conversation, message):
    fbMessage = newMessageMessage(userFrom, conversation, message)
    userTo.sendFireBaseNotification('newMessage', fbMessage['title'], fbMessage['body'], fbMessage['imageURL'], fbMessage['data'])
