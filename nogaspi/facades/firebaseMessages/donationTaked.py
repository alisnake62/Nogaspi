def donationTakedMessage(points):  
    return {
        'data': {
            'points': str(points)
        }
    }
def donationTaked(userOwner, points):
    message = donationTakedMessage(points)

    userOwner.sendFireBaseEvent('donationTaked', message['data'])