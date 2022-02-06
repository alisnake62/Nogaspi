import datetime

from facades.apiConfig import DonationException
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Donation (Base):

    __tablename__ = 'donation'
    id = Column(INTEGER, primary_key=True)
    idUser = Column(INTEGER, ForeignKey('user.id'))
    user = relationship("User", back_populates="donations")
    latitude = Column(FLOAT)
    longitude = Column(FLOAT)
    geoPrecision = Column(INTEGER)
    startingDate = Column(DATE)
    endingDate = Column(DATE)
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

    def isFavorite(self, user):
        if user in self.favoriteUsers:
            return True
        return False

    def toJson(self, user):

        allergens = []
        for article in self.articles:
            allergens += [allergen.toJson() for allergen in article.product.allergens]
        allergens = list(set(allergens))

        toJson = {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'geoPrecision': self.geoPrecision,
            'startingDate': self.startingDate,
            'endingDate': self.endingDate,
            'isExpired': self.isExpired(),
            'isArchived': self.isArchived(),
            'isValide': self.isValide(),
            'articles': [a.toJson() for a in  self.articles],
            'allergens': allergens,
            'owner': self.user.toJson(),
            'isMine': self.user == user,
            'conversationsInfo': [c.toJsonlight(user) for c in self.conversations] if self.user == user else None,
            'isMyFavorite': self.isFavorite(user)
        }

        return toJson