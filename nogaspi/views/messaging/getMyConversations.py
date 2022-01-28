from models.objectDB import Donation, Conversation
from dbEngine import EngineSQLAlchemy
from facades.registerUtils import getUserFromToken
from apiConfig import getArgs
from sqlalchemy import or_

def f(request):

    token, withArchivedDonations, withExpiredDonations = getArgs(request, ['token', 'withArchivedDonations', 'withExpiredDonations'])

    with EngineSQLAlchemy(request) as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        conversations = session.query( Conversation ).filter(or_(user == Conversation.userTaker, user == Conversation.userDonator)).all()

        if withArchivedDonations == '0':
            conversations = [c for c in conversations if not c.donation.isArchived()]
        if withExpiredDonations == '0':
            conversations = [c for c in conversations if not c.donation.isExpired()]

        data = {'conversations': [c.toJson(user) for c in conversations]}
    return data