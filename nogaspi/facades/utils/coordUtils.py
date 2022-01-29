import math
from facades.apiConfig import CoordException

def isAround(coord1, coord2, distance):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    if distanceBetween(lat1, lon1, lat2, lon2) * 1000 <= distance:
        return True
    return False

def isAroundPath(pathPoints, coordCheck, distance):
    latPointCheck, lonPointCheck = coordCheck
    
    for pathPoint in pathPoints:
        latPathPoint = pathPoint["latitude"]
        lonPathPoint = pathPoint["longitude"]
        if distanceBetween(latPointCheck, lonPointCheck, latPathPoint, lonPathPoint) * 1000 <= distance:
            return True
    return False

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