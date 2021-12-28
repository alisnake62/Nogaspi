import secrets
import datetime

from apiConfig import DonationException
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Donation (Base):

    CODE_VALIDITY = 5   #minutes

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
    code = Column(VARCHAR)
    code_expiration = Column(DATETIME)
    archive = Column(BOOLEAN)

    def __init__(self, user, latitude, longitude, geoPrecision, endingDate, archive = False):        
        self.user = user
        self.latitude = latitude
        self.longitude = longitude
        self.geoPrecision = geoPrecision
        self.startingDate = datetime.datetime.now()
        self.endingDate = endingDate
        self.archive = archive

    def generateCode(self):
        self.code = secrets.token_hex()
        self.code_expiration = datetime.datetime.now() + datetime.timedelta(minutes = self.CODE_VALIDITY)
        return {'code': self.code, 'code_expiration': self.code_expiration}

    def isValide(self):
        if self.archive or self.endingDate < datetime.datetime.now():
            return False
        return True
    
    def checkValidityRaiseException(self, request):
        if self.archive:
            message = "This donation is archived"
            raise DonationException(message, message, request)
        elif self.endingDate < datetime.datetime.now():
            message = "This donation is expired"
            raise DonationException(message, message, request)
    
    def compareCodeRaiseException(self, inputCode, request):
        if self.code != inputCode:
            message = "Donation Code Unknown"
            raise DonationException(message, message, request)
        elif self.code_expiration < datetime.datetime.now():
            message = "Donation Code Expired"
            raise DonationException(message, message, request)

    def toJson(self):

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
            'articles': [a.toJson() for a in  self.articles],
            'allergens': allergens,
            'user': self.user.toJson()
        }
        return toJson