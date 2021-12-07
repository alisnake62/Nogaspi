from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Allergen (Base):

    __tablename__ = 'allergen'
    id = Column(INTEGER, primary_key=True)
    nameEN = Column(TEXT)
    nameFR = Column(TEXT)
    articles = relationship("Article", back_populates="allergen")

    def __init__(self, nameEN, nameFR = None):                    
        self.nameEN = nameEN
        self.nameFR = nameFR