import pytest
from nogaspi.dbEngine import EngineSQLAlchemy
from test.functionalTest.dbMagement import sqlDeleteAllData

from nogaspi.facades.utils.cypherUtils import encrypt



def pytest_sessionstart( ):
    with EngineSQLAlchemy() as session:
        session.execute("DROP DATABASE IF EXISTS `nogaspi`;")
        session.execute("CREATE DATABASE `nogaspi`;")
        session.execute("USE `nogaspi`;")
        with open("test/nogaspi.sql", encoding="utf-8") as sql_file:
            for statement in sql_file.read().split(';'):
                if len(statement.strip()) > 0:
                    session.execute(statement + ';')
        session.commit()

def pytest_configure():
    message1 = "message1"
    message2 = "message2"
    message3 = "message3"
    encryptedMessage1 = encrypt(message1)
    encryptedMessage2 = encrypt(message2)
    encryptedMessage3 = encrypt(message3)

    pytest.message1 = message1
    pytest.message2 = message2
    pytest.message3 = message3
    pytest.encryptedMessage1 = encryptedMessage1
    pytest.encryptedMessage2 = encryptedMessage2
    pytest.encryptedMessage3 = encryptedMessage3

@pytest.fixture(autouse=True)
def append_first():
    sqlDeleteAllData()