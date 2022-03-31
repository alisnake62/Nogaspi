import math
import requests
import os
import traceback
from facades.apiConfig import OpenRouteServiceException

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

def isEquals(lat1, lon1, lat2, lon2):
    marge = 0.00005 # ~ 4 meters

    if None in (lat1, lon1, lat2, lon2): return False
    
    return abs(lat1 - lat2) <= marge and abs(lon1 - lon2) <= marge

def getPathPoints(request, latStart, lonStart, latEnd, lonEnd, pathType):

    if os.environ['LAUNCH_ENV'] == 'test': return None

    routeByPathType = {
        "car": "driving-car",
        "bike": "cycling-regular",
        "foot": "foot-walking"
    }

    apiKey = os.environ['OPENROUTESERVICE_KEY']

    headers = {'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'}
    url = f"https://api.openrouteservice.org/v2/directions/{routeByPathType[pathType]}?api_key={apiKey}&start={lonStart},{latStart}&end={lonEnd},{latEnd}"

    try:
        call = requests.get(url, headers=headers)
        if call.status_code != 200: raise Exception()
    except Exception:
        raise OpenRouteServiceException("Problem to access at OpenRoute web Service", traceback.format_exc(), request)

    pathPoints = call.json()['features'][0]['geometry']['coordinates']

    return [{'latitude': lat, 'longitude': lon} for [lon, lat] in pathPoints]