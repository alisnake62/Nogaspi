from models.objectDB.conversation import Conversation
from dbEngine import EngineSQLAlchemy
from facades.utils.registerUtils import getUserFromToken
from facades.apiConfig import getArgs
from sqlalchemy import or_

def getMyConversations(request):

    token, withArchivedDonations, withExpiredDonations = getArgs(request, ['token', 'withArchivedDonations', 'withExpiredDonations'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        conversations = session.query( Conversation ).filter(or_(user == Conversation.userTaker, user == Conversation.userDonator)).all()

        if withArchivedDonations == '0':
            conversations = [c for c in conversations if not c.donation.isArchived()]
        if withExpiredDonations == '0':
            conversations = [c for c in conversations if not c.donation.isExpired()]

        data = {'conversations': [c.toJsonlight(user) for c in conversations]}
    return data