import secrets
import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
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

    def __init__(self, user, latitude, longitude, geoPrecision, endingDate):        
        self.user = user
        self.latitude = latitude
        self.longitude = longitude
        self.geoPrecision = geoPrecision
        self.startingDate = datetime.now()
        self.endingDate = endingDate

    def generateCode(self):
        self.code = secrets.token_hex()
        self.code_expiration = datetime.datetime.now() + datetime.timedelta(minutes = self.CODE_VALIDITY)
        return {'code': self.code, 'code_expiration': self.code_expiration}

    def toJson(self):
        toJson = {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'geoPrecision': self.geoPrecision,
            'startingDate': self.startingDate,
            'endingDate': self.endingDate,
            'articles': [a.toJson() for a in  self.articles],
            'user': self.user.toJson()
        }
        return toJson