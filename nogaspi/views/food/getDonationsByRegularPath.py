from models.objectDB import Donation
from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from facades.coordUtils import isAroundPath
from apiConfig import UserException
import json

def f(request):

    token = request.args.get('token')
    distanceMax = distanceMax = float(request.args.get('distanceMax'))

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        regularPathPoints = json.loads(user.regularPathPoints)
        if regularPathPoints is None:
            message = "you don't have a regular path in your profile"
            raise UserException(message, message, request)
        
        donations = session.query( Donation )

        if filter:
            donations = [d for d in donations if isAroundPath(regularPathPoints, (d.latitude, d.longitude), distanceMax)]

        data = {'donations': [d.toJson(user) for d in donations if d.isValide()]}
    return data