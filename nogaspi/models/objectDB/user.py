import secrets
import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base, EngineSQLAlchemy

class User (Base):

    TOKEN_VALIDITY = 15   #minutes

    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True)
    mail = Column(VARCHAR)
    password = Column(VARCHAR)
    token = Column(VARCHAR)
    token_expiration = Column(DATE)

    def __init__(self, mail : String, password : String):                    
        self.mail = mail             
        self.password = password

    def generateToken(self):
        self.token = secrets.token_hex()
        self.token_expiration = datetime.datetime.now() + datetime.timedelta(minutes = self.TOKEN_VALIDITY)
        return {'token': self.token, 'token_expiration': str(self.token_expiration + datetime.timedelta(minutes = 60)) + " GMT+1"}