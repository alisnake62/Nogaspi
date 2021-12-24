import math

def isAround(coord1, coord2, distance):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    if distanceBetween(lat1, lon1, lat2, lon2) * 1000 > distance:
        return False
    return True

def distanceBetween(lat1, lon1, lat2, lon2):
    if lat1 == lat2 and lon1 == lon2:
        return 0
    else:
        theta = lon1 - lon2
        dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta));
        dist = math.acos(dist)
        dist = math.degrees(dist)
        dist = dist * 60 * 1.1515
        dist *= 1.609344
        return dist

def makeDonation(userOwner, userTaker, donation):
    donation.archive = True
    for article in donation.articles:
        article.fridge = None
    userTaker.points += 5
    userOwner.points += 20