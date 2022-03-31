from facades.const import MAX_LETTER_COUNT_ON_NOTIFICATION

def body(donation):

    productNamesToString = donation.productNameListToNotification()
    productNamesToStringSize = len(productNamesToString)

    if productNamesToStringSize > MAX_LETTER_COUNT_ON_NOTIFICATION: 
        productNamesToString = productNamesToString[:MAX_LETTER_COUNT_ON_NOTIFICATION] + "..."

    return productNamesToString
 
def likeDonationMessage(userFrom, donation):  
    return {
        'title': f"{userFrom.pseudo} aime votre donation",
        'body': body(donation),
        'data': None,
        'imageURL': None
    }
def likeDonation(userFrom, userTo, donation):
    fbMessage = likeDonationMessage(userFrom, donation)
    userTo.sendFireBaseNotification('likeDonation', fbMessage['title'], fbMessage['body'], fbMessage['imageURL'], fbMessage['data'])