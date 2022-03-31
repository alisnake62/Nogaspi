import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship
from facades.utils.cypherUtils import encrypt, decrypt, getEncryptor, getDecryptor
import json

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
        self.postBody(body)

    def postBody(self, messageText):
        encryptor = getEncryptor()
        splitSize = 50
        splitedMessageText = [messageText[y-splitSize:y] for y in range(splitSize, len(messageText)+splitSize,splitSize)]
        encrpytedMessageText = [encrypt(encryptor, part) for part in splitedMessageText]
        self.body = json.dumps(encrpytedMessageText)

    def getBody(self, decryptor = None):
        if decryptor is None: decryptor = getDecryptor()

        encrpytedMessageText = json.loads(self.body)
        splitedMessageText = [decrypt(decryptor, part) for part in encrpytedMessageText]
        return "".join(splitedMessageText)

    def userFrom(self):
        return self.conversation.userTaker if self.toDonator else self.conversation.userDonator

    def userTo(self):
        return self.conversation.userDonator if self.toDonator else self.conversation.userTaker

    def toStringToNotification(self, donation): 
        return f"Message: {self.getBody()}, Donation : {donation.productNameListToNotification()}"
    
    def toJson(self, userRequester, decryptor = None):
        toJson = {
            'id': self.id,
            'readed': self.readed,
            'dateTime': int(datetime.datetime.timestamp(self.dateTime)),
            'body': self.getBody(decryptor),
            'userFrom': self.userFrom().toJson(),
            'userTo': self.userTo().toJson(),
            'isAMessageFromMe': userRequester == self.userFrom()
        }
        return toJson