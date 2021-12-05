import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker

from apiConfig import DBException

Base = declarative_base()

class EngineSQLAlchemy:

    def __enter__(self):
        try:
            password = os.environ['MYSQL_ROOT_PASSWORD']
            host = os.environ['PMA_HOST']
            self.engine = create_engine('mysql+mysqlconnector://root:{}@{}/nogaspi'.format(password, host), echo=False)
            Base.metadata.create_all(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            return self.session

        except Exception as e:
            self.session.close()
            self.engine.dispose()
            print(type(e), e)
            raise DBException("Problem to access at the Database")

    def __exit__(self, type, value, traceback):
        self.session.close()
        self.engine.dispose()