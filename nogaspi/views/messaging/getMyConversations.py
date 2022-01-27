from models.objectDB import Donation, Conversation
from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from sqlalchemy import or_

def f(request):

    token = request.args.get('token')
    withArchivedDonations = request.args.get('withArchivedDonations') == "1"
    withExpiredDonations = request.args.get('withExpiredDonations') == "1"

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        conversations = session.query( Conversation ).filter(or_(user == Conversation.userTaker, user == Conversation.userDonator)).all()

        if not withArchivedDonations:
            conversations = [c for c in conversations if not c.donation.isArchived()]
        if not withExpiredDonations:
            conversations = [c for c in conversations if not c.donation.isExpired()]

        data = {'conversations': [c.toJson(user) for c in conversations]}
    return data