from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship
from facades.apiConfig import ConversationException
import datetime

from dbEngine import Base

class Conversation (Base):

    __tablename__ = 'conversation'
    id = Column(INTEGER, primary_key=True)
    idDonation = Column(INTEGER, ForeignKey('donation.id'))
    donation = relationship("Donation", back_populates="conversations")
    idUserDonator = Column(INTEGER, ForeignKey('userNogaspi.id'))
    idUserTaker = Column(INTEGER, ForeignKey('userNogaspi.id'))
    userDonator = relationship("User", back_populates="conversationsDonator", foreign_keys=idUserDonator)
    userTaker = relationship("User", back_populates="conversationsTaker", foreign_keys=idUserTaker)
    messages = relationship("Message", back_populates="conversation")

    def __init__(self, donation, userDonator, userTaker):        
        self.donation = donation
        self.userDonator = userDonator
        self.userTaker = userTaker

    def checkLegitimacyRaiseException(self, userRequester, checkDonationValidity, request):
        if checkDonationValidity: self.donation.checkValidityRaiseException(request)

        if not userRequester in (self.userDonator, self.userTaker):
            message = "You can't interact with this conversation, it's not yours"
            raise ConversationException(message, message, request)

    def toJson(self, userRequester):
        self.messages.sort(key=lambda r: r.dateTime)

        toJson = {
            'id': self.id,
            'idDonation': self.idDonation,
            'isMyDonation': userRequester == self.userDonator,
            'dateBeginning': int(datetime.datetime.timestamp(self.messages[0].dateTime)),
            'lastMessage': self.messages[-1].toJson(userRequester),
            'userDonator': self.userDonator.toJson(),
            'userTaker': self.userTaker.toJson(),
            'messages': [message.toJson(userRequester) for message in self.messages],
            'donationIsExpired': self.donation.isExpired(),
            'donationIsArchived': self.donation.isArchived(),
            'donationIsValide': self.donation.isValide()
        }
        return toJson

    def toJsonlight(self, userRequester):

        toJson = self.toJson(userRequester)
        del toJson['messages']
        return toJson
