from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship

from dbEngine import Base

class FavoriteDonation(Base):
    __tablename__ = "favorite_donation"
    id = Column(Integer, primary_key=True)
    idUser = Column(Integer, ForeignKey('userNogaspi.id'))
    idDonation = Column(Integer, ForeignKey('donation.id'))

    def __init__(self, idUser, idDonation):
        self.idUser = idUser
        self.idDonation = idDonation