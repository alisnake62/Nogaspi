import math
from apiConfig import CoordException

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

def checkCoordRaiseException(coord, request):
    lat, lon = coord
    if lat < -90 or lat > 90:
        message = f"Latitude {lat} is not valid"
        raise CoordException(message, message, request)
    if lon < -180 or lat > 180:
        message = f"Longitude {lon} is not valid"
        raise CoordException(message, message, request)