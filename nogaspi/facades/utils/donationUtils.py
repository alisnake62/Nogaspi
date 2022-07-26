from datetime import datetime
from models.objectDB import User, Donation
from facades.const import DISTANCE_MAX_TO_SEND_NOTIFICATION_IN_NEW_DONATION, MAX_DONATION_PER_DAY_ON_UNIT_TEST, MAX_DONATION_PER_DAY_ON_PROD, POINT_PER_DONATED_ARTICLE, POINT_PER_TAKED_ARTICLE
from facades.utils.coordUtils import isAroundPath
from facades.firebaseMessages.newNearDonation import newNearDonation
import os
from sqlalchemy import extract

def makeDonation(userOwner, userTaker, donation):
    donation.archive = True
    donation.userTaker = userTaker
    articleCount = len(donation.articles)
    for article in donation.articles:
        article.fridge = None
    userTaker.points += articleCount * POINT_PER_TAKED_ARTICLE
    userOwner.points += articleCount * POINT_PER_DONATED_ARTICLE
    return articleCount * POINT_PER_DONATED_ARTICLE

def updateRatingUser(user, note):
    ratingCount = user.ratingCount
    rating = user.rating
    newRating = (rating * ratingCount + note) / (ratingCount + 1)
    user.rating = newRating
    user.ratingCount = ratingCount + 1

def sendFireBaseNotificationsOneNewNearDonation(session, donation):
    coordToCheck = (donation.latitude, donation.longitude)
    usersToCheck = session.query( User ).filter(
        User.isConfirmate == 1,
        User.regularPathPoints != None,
        User != donation.user
    ).all()

    usersToSend = []
    for user in usersToCheck:
        if isAroundPath(user.regularPath(False), coordToCheck, DISTANCE_MAX_TO_SEND_NOTIFICATION_IN_NEW_DONATION):
            usersToSend.append(user)

    if usersToSend != []:
        newNearDonation(usersToSend, donation)

def donationIsOnQuota(user, session):
    maxDonationPerDay = MAX_DONATION_PER_DAY_ON_UNIT_TEST if os.environ['LAUNCH_ENV'] == 'test' else MAX_DONATION_PER_DAY_ON_PROD
    donationCountToday = session.query( Donation ).filter(
        Donation.user == user,
        extract('year', Donation.startingDate) == datetime.now().year,
        extract('month', Donation.startingDate) == datetime.now().month,
        extract('day', Donation.startingDate) == datetime.now().day
    ).count()

    return donationCountToday < maxDonationPerDay