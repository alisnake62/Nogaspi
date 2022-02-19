import datetime

from facades.apiConfig import DonationException
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Donation (Base):

    __tablename__ = 'donation'
    id = Column(INTEGER, primary_key=True)
    idUser = Column(INTEGER, ForeignKey('userNogaspi.id'))
    user = relationship("User", back_populates="donations")
    latitude = Column(FLOAT)
    longitude = Column(FLOAT)
    geoPrecision = Column(INTEGER)
    startingDate = Column(DATETIME)
    endingDate = Column(DATETIME)
    articles = relationship("Article", back_populates="donation")
    idDonationCode = Column(INTEGER, ForeignKey('donationCode.id'))
    donationCode = relationship("DonationCode", back_populates="donations")
    archive = Column(BOOLEAN)
    favoriteUsers = relationship("User", secondary='favorite_donation', back_populates="favoriteDonations")
    conversations = relationship("Conversation", back_populates="donation")

    def __init__(self, user, latitude, longitude, geoPrecision, endingDate, archive = False):        
        self.user = user
        self.latitude = latitude
        self.longitude = longitude
        self.geoPrecision = geoPrecision
        self.startingDate = datetime.datetime.now()
        self.endingDate = endingDate
        self.archive = archive

    def isValide(self):
        if self.archive or self.endingDate < datetime.datetime.now():
            return False
        return True

    def isArchived(self):
        return self.archive

    def isExpired(self):
        if self.endingDate < datetime.datetime.now():
            return True
        return False
    
    def checkValidityRaiseException(self, request):
        if self.archive:
            message = "This donation is archived"
            raise DonationException(message, message, request)
        elif self.endingDate < datetime.datetime.now():
            message = "This donation is expired"
            raise DonationException(message, message, request)

    def isFavorite(self, userRequester):
        if userRequester in self.favoriteUsers:
            return True
        return False

    def toJson(self, userRequester):

        allergens = []
        for article in self.articles:
            allergens += [allergen.toJson() for allergen in article.product.allergens]
        allergens = list(set(allergens))

        myTakerConversationInfo = None
        for conversation in self.conversations:
            if conversation.userTaker == userRequester:
                myTakerConversationInfo = conversation.toJsonlight(userRequester)
                break

        toJson = {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'geoPrecision': self.geoPrecision,
            'startingDate': int(datetime.datetime.timestamp(self.startingDate)),
            'endingDate': int(datetime.datetime.timestamp(self.endingDate)),
            'isExpired': self.isExpired(),
            'isArchived': self.isArchived(),
            'isValide': self.isValide(),
            'articles': [a.toJson() for a in  self.articles],
            'allergens': allergens,
            'owner': self.user.toJson(),
            'isMine': self.user == userRequester,
            'myTakerConversationInfo': myTakerConversationInfo,
            'myDonatorConversationsInfo': [c.toJsonlight(userRequester) for c in self.conversations] if self.user == userRequester else None,
            'isMyFavorite': self.isFavorite(userRequester)
        }

        return toJson