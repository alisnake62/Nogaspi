from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Allergen (Base):

    __tablename__ = 'allergen'
    id = Column(INTEGER, primary_key=True)
    nameEN = Column(VARCHAR)
    nameFR = Column(VARCHAR)
    articles = relationship("Article", secondary='article_allergen', back_populates="allergens")

    def __init__(self, nameEN, nameFR = None):                    
        self.nameEN = nameEN
        self.nameFR = nameFR

    def toJson(self):
        if self.nameFR is None: return self.nameEN
        else : return self.nameFR