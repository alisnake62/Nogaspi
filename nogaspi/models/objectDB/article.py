import datetime


from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
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
    ingredient = Column(TEXT)
    idLastScanUser = Column(INTEGER, ForeignKey('user.id'))
    lastUserScan = relationship("User", back_populates="articles")
    lastScanDate = Column(DATETIME)

    def __init__(self, name, quantity, lastUserScanId, opinion=None, brand=None, barcode=None, image_url=None, ingredient=None):                    
        self.opinion = opinion        
        self.brand = brand
        self.name = name
        self.quantity = quantity
        self.barcode = barcode
        self.image_url = image_url
        self.lastUserScanId = lastUserScanId
        self.ingredient = ingredient

    def majInfoLastScan(self, user):
        self.lastScanDate = datetime.datetime.now()
        self.lastUserScan = user