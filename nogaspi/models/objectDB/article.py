from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Article (Base):

    __tablename__ = 'article'
    id = Column(INTEGER, primary_key=True)
    opinion = Column(TEXT)
    brand = Column(VARCHAR)
    name = Column(VARCHAR)
    quantity = Column(VARCHAR)
    barcode = Column(VARCHAR)
    image_url = Column(VARCHAR)

    def __init__(self, name, quantity, opinion=None, brand=None, barcode=None, image_url=None):                    
        self.opinion = opinion        
        self.brand = brand
        self.name = name
        self.quantity = quantity
        self.barcode = barcode
        self.image_url = image_url