from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.utils.coordUtils import isAroundPath
from facades.apiConfig import UserException, getArgs
import json

def getDonationsByRegularPath(request):

    token, distanceMax, = getArgs(request, ['token', 'distanceMax'])
    distanceMax = float(distanceMax)

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        regularPathPoints = user.regularPath()
        if regularPathPoints is None:
            message = "you don't have a regular path in your profile"
            raise UserException(message, message, request)
        
        donations = session.query( Donation )

        if filter:
            donations = [d for d in donations if isAroundPath(regularPathPoints, (d.latitude, d.longitude), distanceMax)]

        data = {'donations': [d.toJson(user) for d in donations if d.isValide()]}
    return data