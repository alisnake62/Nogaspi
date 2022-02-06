from datetime import date, timedelta
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, FLOAT, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Fridge (Base):

    __tablename__ = 'fridge'
    id = Column(INTEGER, primary_key=True)
    idUser = Column(INTEGER, ForeignKey('userNogaspi.id'))
    user = relationship("User", back_populates="fridges")
    articles = relationship("Article", back_populates="fridge")


    def __init__(self, user):        
        self.user = user

    def toJson(self):
        toJson = {            
            'articles': [a.toJson() for a in self.articles if (a.expirationDate + timedelta(days=15)) >= date.today()]
        }
        return toJson