def likeDonationMessage(userFrom, donation):  
    return {
        'title': f"{userFrom.pseudo} aime votre donation",
        'body': f"Donation {donation.id}",
        'data': None,
        'imageURL': None
    }
def likeDonation(userFrom, userTo, donation):
    message = likeDonationMessage(userFrom, donation)
    userTo.sendFireBaseNotification('newMessage', message['title'], message['body'], message['imageURL'], message['data'])