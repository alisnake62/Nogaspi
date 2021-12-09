from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Donation (Base):

    __tablename__ = 'donation'
    id = Column(INTEGER, primary_key=True)
    idArticle = Column(INTEGER, ForeignKey('article.id'))
    article = relationship("Article", back_populates="donations")
    idUser = Column(INTEGER, ForeignKey('user.id'))
    user = relationship("User", back_populates="donations")
    expirationDate = Column(DATETIME)
    latitude = Column(FLOAT)
    longitude = Column(FLOAT)
    geoPrecision = Column(INTEGER)

    def __init__(self, idArticle, idUser, expirationDate, latitude, longitude, geoPrecision):        
        self.idArticle = idArticle
        self.idUser = idUser
        self.expirationDate = expirationDate
        self.latitude = latitude
        self.longitude = longitude
        self.geoPrecision = geoPrecision

    def toJson(self):
        toJson = {
            'id': self.id,
            'article': self.article.toJson(),
            'expirationDate': self.expirationDate,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'geoPrecision': self.geoPrecision
        }
        return toJson