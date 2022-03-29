from facades.utils.fireBaseUtils import sendNotificationMultiUser

def newNearDonationMessage(donation):  
    return {
        'title': "Une nouvelle donation proche de votre chemin",
        'body': f"Donation {donation.id} de la part de {donation.user.pseudo}",
        'data': {
            "userDonation": donation.user.pseudo,
            "idDonation": str(donation.id)
        },
        'imageURL': None
    }
def newNearDonation(users, donation):
    message = newNearDonationMessage(donation)
    firebaseTokens = [user.fireBaseToken for user in users if user.fireBaseToken]
    sendNotificationMultiUser('newMessage', message['title'], message['body'], message['imageURL'], message['data'])