def likeDonationNotif(userFrom, donation):  
    return {
        'title': f"{userFrom.pseudo} aime votre donation",
        'body': f"Donation {donation.id}",
        'data': None,
        'imageURL': None
    }
def likeDonation(userFrom, userTo, donation):
    notif = likeDonationNotif(userFrom, donation)
    userTo.sendFireBaseNotification(notif['title'], notif['body'], notif['data'], notif['imageURL'])
