import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Message (Base):

    __tablename__ = 'message'
    id = Column(INTEGER, primary_key=True)
    idConversation = Column(INTEGER, ForeignKey('conversation.id'))
    conversation = relationship("Conversation", back_populates="messages")
    toDonator = Column(BOOLEAN)
    readed = Column(BOOLEAN)
    dateTime = Column(DATETIME)
    body = Column(TEXT)

    def __init__(self, conversation, toDonator, body):        
        self.conversation = conversation
        self.toDonator = toDonator
        self.readed = False
        self.dateTime = datetime.datetime.now()
        self.body = body

    def toJson(self, userRequester):
        
        userFrom = self.conversation.userTaker if self.toDonator else self.conversation.userDonator
        userTo = self.conversation.userDonator if self.toDonator else self.conversation.userTaker

        toJson = {
            'id': self.id,
            'readed': self.readed,
            'dateTime': self.dateTime,
            'body': self.body,
            'userFrom': userFrom.toJson(),
            'userTo': userTo.toJson(),
            'isAMessageFromMe': userRequester == userFrom
        }
        return toJson