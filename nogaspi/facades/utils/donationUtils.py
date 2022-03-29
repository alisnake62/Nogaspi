from models.objectDB import User
from facades.const import DISTANCE_MAX_TO_SEND_NOTIFICATION_IN_NEW_DONATION
from facades.utils.coordUtils import isAroundPath
from facades.firebaseMessages.newNearDonation import newNearDonation

def makeDonation(userOwner, userTaker, donation):
    donation.archive = True
    donation.userTaker = userTaker
    articleCount = len(donation.articles)
    for article in donation.articles:
        article.fridge = None
    userTaker.points += articleCount
    userOwner.points += articleCount * 4
    return articleCount * 4

def updateRatingUser(user, note):
    ratingCount = user.ratingCount
    rating = user.rating
    newRating = (rating * ratingCount + note) / (ratingCount + 1)
    user.rating = newRating
    user.ratingCount = ratingCount + 1

def sendFireBaseNotificationsOneNewNearDonation(session, donation):
    coordToCheck = (donation.latitude, donation.longitude)
    usersToCheck = session.query( User ).filter(User.isConfirmate, User.regularPathPoints).all()

    usersToSend = []
    for user in usersToCheck:
        if isAroundPath(user.regularPath(False), coordToCheck, DISTANCE_MAX_TO_SEND_NOTIFICATION_IN_NEW_DONATION):
            usersToSend.append(user)

    newNearDonation(usersToSend, donation)