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

def checkDonationCode(donation, donationCode, request):
    if donation.code != donationCode:
        message = "Donation Code Unknown"
        raise DonationException(message, message, request)
    elif donation.code_expiration < datetime.datetime.now():
        message = "Donation Code Expired"
        raise DonationException(message, message, request)