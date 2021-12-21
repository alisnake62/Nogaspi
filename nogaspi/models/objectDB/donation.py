from datetime import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
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


    def __init__(self, user, latitude, longitude, geoPrecision, endingDate):        
        self.user = user
        self.latitude = latitude
        self.longitude = longitude
        self.geoPrecision = geoPrecision
        self.startingDate = datetime.now()
        self.endingDate = endingDate

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