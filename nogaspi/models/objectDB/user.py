import secrets
import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class User (Base):

    TOKEN_VALIDITY = 1440   #minutes

    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True)
    mail = Column(VARCHAR)
    password = Column(VARCHAR)
    pseudo = Column(VARCHAR)
    token = Column(VARCHAR)
    token_expiration = Column(DATETIME)
    products = relationship("Product", back_populates="lastUserScan")
    points = Column(INTEGER)
    idrang = Column(INTEGER, ForeignKey('rang.id'))
    rang = relationship("Rang", back_populates="users")
    donations = relationship("Donation", back_populates="user")
    fridges = relationship("Fridge", back_populates="user")

    def __init__(self, mail : String, password : String, pseudo):                    
        self.mail = mail             
        self.password = password
        self.pseudo = pseudo

    def generateToken(self):
        self.token = secrets.token_hex()
        self.token_expiration = datetime.datetime.now() + datetime.timedelta(minutes = self.TOKEN_VALIDITY)
        return {'token': self.token, 'token_expiration': self.token_expiration}

    def majTokenValidity(self):
        self.token_expiration = datetime.datetime.now() + datetime.timedelta(minutes = self.TOKEN_VALIDITY)

    def toJson(self):
        toJson = {
            'mail': self.mail,
            'pseudo': self.pseudo,
            'points': self.points,
        }
        return toJson