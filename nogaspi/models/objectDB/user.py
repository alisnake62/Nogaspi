import secrets
import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey, FLOAT
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, JSON, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship
from facades import fireBaseUtils

from dbEngine import Base

class User (Base):

    TOKEN_VALIDITY = 1440   #minutes

    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True)
    mail = Column(VARCHAR)
    password = Column(VARCHAR)
    pseudo = Column(VARCHAR)
    profilePicture = Column(VARCHAR)
    token = Column(VARCHAR)
    token_expiration = Column(DATETIME)
    products = relationship("Product", back_populates="lastUserScan")
    points = Column(INTEGER)
    idrang = Column(INTEGER, ForeignKey('rang.id'))
    rang = relationship("Rang", back_populates="users")
    regularPathLatitudeStart = Column(FLOAT)
    regularPathLongitudeStart = Column(FLOAT)
    regularPathLatitudeEnd = Column(FLOAT)
    regularPathLongitudeEnd = Column(FLOAT)
    regularPathPoints = Column(JSON)
    donations = relationship("Donation", back_populates="user")
    fridges = relationship("Fridge", back_populates="user")
    favoriteDonations = relationship("Donation", secondary='favorite_donation', back_populates="favoriteUsers")
    fireBaseToken = Column(VARCHAR)

    def __init__(self, mail, password, pseudo, profilePicture):                    
        self.mail = mail             
        self.password = password
        self.pseudo = pseudo
        self.profilePicture = profilePicture

    def generateToken(self):
        self.token = secrets.token_hex()
        self.token_expiration = datetime.datetime.now() + datetime.timedelta(minutes = self.TOKEN_VALIDITY)
        return {'token': self.token, 'token_expiration': self.token_expiration}

    def majTokenValidity(self):
        self.token_expiration = datetime.datetime.now() + datetime.timedelta(minutes = self.TOKEN_VALIDITY)

    def killToken(self):
        self.token = None
        self.token_expiration = None

    def sendFireBaseNotification(self, title, body):
        if self.fireBaseToken:
            fireBaseUtils.sendNotification(self.fireBaseToken, title, body)

    def getProfilePicturePath(self):
        return f"images/users/{self.profilePicture}"

    def toJson(self):
        toJson = {
            'mail': self.mail,
            'pseudo': self.pseudo,
            'points': self.points,
        }
        return toJson