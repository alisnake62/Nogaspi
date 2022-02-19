import secrets
import datetime

from facades.apiConfig import DonationException
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship
from facades.const import DONATION_CODE_VALIDITY

from dbEngine import Base

class DonationCode (Base):

    __tablename__ = 'donationCode'
    id = Column(INTEGER, primary_key=True)
    code = Column(VARCHAR)
    expirationDate = Column(DATETIME)
    donations = relationship("Donation", back_populates="donationCode")

    def __init__(self):        
        self.code = secrets.token_hex()
        self.expirationDate = datetime.datetime.now() + datetime.timedelta(minutes = DONATION_CODE_VALIDITY)

    def isValide(self):
        return self.expirationDate > datetime.datetime.now()

    def userOwner(self):
        return self.donations[0].user

    def toJson(self):
        toJson = {
            'code': self.code,
            'expirationDate': int(datetime.datetime.timestamp(self.expirationDate))
        }
        return toJson