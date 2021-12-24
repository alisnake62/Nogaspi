from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class ArticleAllergen(Base):
    __tablename__ = "article_allergen"

    id = Column(Integer, primary_key=True)
    idArticle = Column(Integer, ForeignKey('article.id'))
    idAllergen = Column(Integer, ForeignKey('allergen.id'))