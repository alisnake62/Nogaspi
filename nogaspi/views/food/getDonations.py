from models.objectDB import Article, Donation
from dbEngine import EngineSQLAlchemy
from apiConfig import EmptyException
from facades.registerUtils import getUserFromToken
from facades.donationUtils import getCoordMinMaxAroundDistance


def f(request):

    token = request.args.get('token')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    geoPrecision = request.args.get('geoPrecision')

    filter = False
    if None not in (latitude, longitude, geoPrecision):
        filter = True
        latitude, longitude, geoPrecision = (float(a) for a in (latitude, longitude, geoPrecision))
        coordStart = (latitude, longitude)

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        if filter:
            latMin, latMax, lonMin, lonMax = getCoordMinMaxAroundDistance(coordStart, geoPrecision)
            donations = session.query( Donation ).filter(Donation.latitude.between(latMin, latMax), Donation.longitude.between(lonMin, lonMax))
        else:
            donations = session.query( Donation )

        data = {'donations': [d.toJson() for d in donations]}
    return data