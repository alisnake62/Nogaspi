from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class ProductAllergen(Base):
    __tablename__ = "product_allergen"

    id = Column(Integer, primary_key=True)
    idProduct = Column(Integer, ForeignKey('product.id'))
    idAllergen = Column(Integer, ForeignKey('allergen.id'))