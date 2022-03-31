def donationTakedMessage(points):  
    return {
        'data': {
            'points': str(points)
        }
    }
def donationTaked(userOwner, points):
    fbMessage = donationTakedMessage(points)

    userOwner.sendFireBaseEvent('donationTaked', fbMessage['data'])