from facades.const import MAX_LETTER_COUNT_ON_NOTIFICATION

def body(donation, message):

    body = message.toStringToNotification(donation)

    bodySize = len(body)

    if bodySize > MAX_LETTER_COUNT_ON_NOTIFICATION: 
        body = body[:MAX_LETTER_COUNT_ON_NOTIFICATION] + "..."

    return body

def newConversationMessage(userFrom, conversation, message):  
    return {
        'title': f"{userFrom.pseudo} veut vous parler",
        'body': body(conversation.donation, message),
        'data': {
            "userFrom": userFrom.pseudo,
            "idDonation": str(conversation.donation.id),
            "idConversation": str(conversation.id)
        },
        'imageURL': None
    }
def newConversation(userFrom, userTo, conversation, message):
    fbMessage = newConversationMessage(userFrom, conversation, message)
    userTo.sendFireBaseNotification('newConversation', fbMessage['title'], fbMessage['body'], fbMessage['imageURL'], fbMessage['data'])