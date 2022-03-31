def messageReadedMessage(conversation):  
    return {
        'data': {
            'conversationId': str(conversation.id)
        }
    }
def messageReaded(userFrom, conversation):
    fbMessage = messageReadedMessage(conversation)

    userFrom.sendFireBaseEvent('messageReaded', fbMessage['data'])