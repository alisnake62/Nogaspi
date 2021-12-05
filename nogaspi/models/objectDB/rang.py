from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class Rang (Base):

    __tablename__ = 'rang'
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    users = relationship("User", back_populates="rang")