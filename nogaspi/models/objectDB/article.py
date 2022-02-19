import datetime
import json

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Article (Base):

    __tablename__ = 'article'
    id = Column(INTEGER, primary_key=True)
    idProduct = Column(INTEGER, ForeignKey('product.id'))
    product = relationship("Product", back_populates="articles")
    idDonation = Column(INTEGER, ForeignKey('donation.id'))
    donation = relationship("Donation", back_populates="articles")
    expirationDate = Column(DATETIME)
    idFridge = Column(INTEGER, ForeignKey('fridge.id'))
    fridge = relationship("Fridge", back_populates="articles")

    def __init__(self, product, donation, expirationDate, fridge):                    
        self.product = product
        self.donation = donation
        self.expirationDate = expirationDate
        self.fridge = fridge

    def toJson(self):
        toJson = {
            'id': self.id,
            'product': self.product.toJson(),
            'expirationDate': int(datetime.datetime.timestamp(self.expirationDate))
        }
        return toJson