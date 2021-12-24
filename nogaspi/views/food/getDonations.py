from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from facades.donationUtils import isAround

def f(request):

    token = request.args.get('token')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    distanceMax = request.args.get('distanceMax')

    filter = False
    if None not in (latitude, longitude, distanceMax):
        filter = True
        latitude, longitude, distanceMax = (float(a) for a in (latitude, longitude, distanceMax))
        coordUser = (latitude, longitude)

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()
        
        donations = session.query( Donation )

        if filter:
            donations = [d for d in donations if isAround(coordUser, (d.latitude, d.longitude), distanceMax)]

        data = {'donations': [d.toJson() for d in donations if d.isValide()]}
    return data