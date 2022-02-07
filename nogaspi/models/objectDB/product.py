import datetime
import json

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Product (Base):

    __tablename__ = 'product'
    id = Column(INTEGER, primary_key=True)
    opinion = Column(TEXT)
    brand = Column(VARCHAR)
    name = Column(VARCHAR)
    quantity = Column(VARCHAR)
    barcode = Column(VARCHAR)
    image_url = Column(VARCHAR)
    ingredients = Column(TEXT)
    nutrimentData = Column(TEXT)
    nutriscoreData = Column(TEXT)
    allergens = relationship("Allergen", secondary='product_allergen', back_populates="products")
    idLastScanUser = Column(INTEGER, ForeignKey('userNogaspi.id'))
    lastUserScan = relationship("User", back_populates="products")
    lastScanDate = Column(DATETIME)
    articles = relationship("Article", back_populates="product")

    def __init__(self, lastUserScan, lastScanDate, barcode, name = None, quantity = None, opinion=None, brand=None, image_url=None, ingredients=None, nutrimentData = None, nutriscoreData = None):                    
        self.opinion = opinion        
        self.brand = brand
        self.name = name
        self.quantity = quantity
        self.barcode = barcode
        self.image_url = image_url
        self.lastUserScan = lastUserScan
        self.lastScanDate = lastScanDate
        self.ingredients = ingredients
        self.nutrimentData = nutrimentData
        self.nutriscoreData = nutriscoreData

    def majInfoLastScan(self, user):
        self.lastScanDate = datetime.datetime.now()
        self.lastUserScan = user

    def toJson(self):
        toJson = {
            'id': self.id,
            'opinion': self.opinion,
            'name': self.name,
            'brand': self.brand,
            'quantity': self.quantity,
            'barcode': self.barcode,
            'image_url': self.image_url,
            'ingredient' : self.ingredients,
            'nutrimentsData' : None if self.nutrimentData is None else json.loads(self.nutrimentData),
            'nutriscoreData' : None if self.nutriscoreData is None else json.loads(self.nutriscoreData),
            'allergens': [a.toJson() for a in  self.allergens]
        }
        return toJson