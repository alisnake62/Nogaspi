import secrets
import datetime

from facades.apiConfig import DonationException
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class DonationCode (Base):

    CODE_VALIDITY = 5   #minutes

    __tablename__ = 'donationCode'
    id = Column(INTEGER, primary_key=True)
    code = Column(VARCHAR)
    expirationDate = Column(DATETIME)
    donations = relationship("Donation", back_populates="donationCode")

    def __init__(self):        
        self.code = secrets.token_hex()
        self.expirationDate = datetime.datetime.now() + datetime.timedelta(minutes = self.CODE_VALIDITY)

    def isValide(self):
        return self.expirationDate > datetime.datetime.now()

    def toJson(self):
        toJson = {
            'code': self.code,
            'expirationDate': self.expirationDate
        }
        return toJson