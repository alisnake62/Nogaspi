import pytest
from nogaspi.dbEngine import EngineSQLAlchemy
from test.functionalTest.dbMagement import sqlDeleteAllData

def pytest_sessionstart( ):
    with EngineSQLAlchemy() as session:
        session.execute("DROP DATABASE IF EXISTS `nogaspi`;")
        with open("test/nogaspi.sql", encoding="utf-8") as sql_file:
            for statement in sql_file.read().split(';'):
                if len(statement.strip()) > 0:
                    session.execute(statement + ';')
        session.commit()

#def pytest_sessionfinish( ):
#    with EngineSQLAlchemy() as session:
#        sqlDeleteAllData()

@pytest.fixture(autouse=True)
def append_first():
    sqlDeleteAllData()