import datetime
import geopy
import geopy.distance
from apiConfig import DonationException
from geopy.units import meters

def getCoordMinMaxAroundDistance(coordStart, distance):

    start = geopy.Point(coordStart)
    d = geopy.distance.distance(meters = distance)

    latMin = d.destination(point=start, bearing=180).latitude
    latMax = d.destination(point=start, bearing=0).latitude
    lonMin = d.destination(point=start, bearing=270).longitude
    lonMax = d.destination(point=start, bearing=90).longitude

    return latMin, latMax, lonMin, lonMax

def makeDonation(userOwner, userTaker, donation):
    donation.archive = True
    for article in donation.articles:
        article.fridge = None
    userTaker.points += 5
    userOwner.points += 20