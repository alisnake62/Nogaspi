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
    fbMessage = newNearDonationMessage(donation)
    firebaseTokens = [user.fireBaseToken for user in users if user.fireBaseToken]
    sendNotificationMultiUser(firebaseTokens, 'newNearDonation', fbMessage['data'], fbMessage['title'], fbMessage['body'], fbMessage['imageURL'])