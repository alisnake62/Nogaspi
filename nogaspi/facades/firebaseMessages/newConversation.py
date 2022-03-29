def newConversationMessage(userFrom, conversation, messageBody):  
    return {
        'title': f"{userFrom.pseudo} veut vous parler",
        'body': f"Donation {conversation.donation.id}: {messageBody}",
        'data': {
            "userFrom": userFrom.pseudo,
            "idDonation": str(conversation.donation.id),
            "idConversation": str(conversation.id)
        },
        'imageURL': None
    }
def newConversation(userFrom, userTo, conversation, messageBody):
    message = newConversationMessage(userFrom, conversation, messageBody)
    userTo.sendFireBaseNotification('newConversation', message['title'], message['body'], message['imageURL'], message['data'])