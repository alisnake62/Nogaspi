from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship
from apiConfig import ConversationException

from dbEngine import Base

class Conversation (Base):

    __tablename__ = 'conversation'
    id = Column(INTEGER, primary_key=True)
    idDonation = Column(INTEGER, ForeignKey('donation.id'))
    donation = relationship("Donation", back_populates="conversations")
    idUserDonator = Column(INTEGER, ForeignKey('user.id'))
    idUserTaker = Column(INTEGER, ForeignKey('user.id'))
    userDonator = relationship("User", back_populates="conversationsDonator", foreign_keys=idUserDonator)
    userTaker = relationship("User", back_populates="conversationsTaker", foreign_keys=idUserTaker)
    messages = relationship("Message", back_populates="conversation")

    def __init__(self, donation, userDonator, userTaker):        
        self.donation = donation
        self.userDonator = userDonator
        self.userTaker = userTaker

    def checkLegitimacyRaiseException(self, userRequester, request):
        self.donation.checkValidityRaiseException(request)

        if not userRequester in (self.userDonator, self.userTaker):
            message = "You can't interact with this conversation, it's not yours"
            raise ConversationException(message, message, request)