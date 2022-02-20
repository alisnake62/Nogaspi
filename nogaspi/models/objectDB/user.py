import secrets
import datetime
import os

from sqlalchemy import Column, Integer, Text, ForeignKey, FLOAT
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, JSON, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship
from facades.utils import fireBaseUtils
from facades.const import TOKEN_VALIDITY

from dbEngine import Base

class User (Base):
    __tablename__ = 'userNogaspi'
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
    donations = relationship("Donation", foreign_keys="Donation.idUser", back_populates="user")
    fridges = relationship("Fridge", back_populates="user")
    favoriteDonations = relationship("Donation", secondary='favorite_donation', back_populates="favoriteUsers")
    fireBaseToken = Column(VARCHAR)
    conversationsDonator = relationship("Conversation", foreign_keys="Conversation.idUserDonator", back_populates="userDonator")
    conversationsTaker = relationship("Conversation", foreign_keys="Conversation.idUserTaker", back_populates="userTaker")
    donationsTaked = relationship("Donation", foreign_keys="Donation.idUserTaker", back_populates="userTaker")
    rating = Column(FLOAT)
    ratingCount = Column(INTEGER)

    def __init__(self, mail, password, pseudo, profilePicture):                    
        self.mail = mail             
        self.password = password
        self.pseudo = pseudo
        self.profilePicture = profilePicture
        self.points = 0
        self.rating = 0.0
        self.ratingCount = 0

    def generateToken(self):
        self.token = secrets.token_hex()
        self.token_expiration = datetime.datetime.now() + datetime.timedelta(minutes = TOKEN_VALIDITY)
        return {'token': self.token, 'token_expiration': self.token_expiration}

    def majTokenValidity(self):
        self.token_expiration = datetime.datetime.now() + datetime.timedelta(minutes = TOKEN_VALIDITY)

    def killToken(self):
        self.token = None
        self.token_expiration = None
        self.fireBaseToken = None

    def profilePictureURL(self):
        profilePicture = self.profilePicture if self.profilePicture else "emptyProfile.jpg"
        return f"http://{os.environ['SERVER_ADRESS']}:49080/users/{profilePicture}"

    def sendFireBaseNotification(self, title, body, data = None, imageURL=None):
        if self.fireBaseToken:
            fireBaseUtils.sendNotification(self.fireBaseToken, title, body, data, imageURL)

    def toJson(self):
        toJson = {
            'id': self.id,
            'mail': self.mail,
            'pseudo': self.pseudo,
            'points': self.points,
            'profilePictureUrl': self.profilePictureURL(),
            'rating':{
                'average': self.rating,
                'count': self.ratingCount
            }
        }
        return toJson