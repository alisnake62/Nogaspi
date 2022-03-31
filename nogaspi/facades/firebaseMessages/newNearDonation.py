from facades.utils.fireBaseUtils import sendNotificationMultiUser
from facades.const import MAX_LETTER_COUNT_ON_NOTIFICATION


def body(donation):

    productNamesToString = donation.productNameListToNotification()
    productNamesToStringSize = len(productNamesToString)

    if productNamesToStringSize > MAX_LETTER_COUNT_ON_NOTIFICATION: 
        productNamesToString = productNamesToString[:MAX_LETTER_COUNT_ON_NOTIFICATION] + "..."

    return productNamesToString

def newNearDonationMessage(donation):  
    return {
        'title': "Une nouvelle donation proche de votre chemin",
        'body': body(donation),
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