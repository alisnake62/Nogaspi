import pytest
from nogaspi.dbEngine import EngineSQLAlchemy

def pytest_sessionstart( ):
    with EngineSQLAlchemy() as session:
        session.execute("DROP DATABASE IF EXISTS `nogaspi`;")
        with open("test/nogaspi.sql", encoding="utf-8") as sql_file:
            for statement in sql_file.read().split(';'):
                if len(statement.strip()) > 0:
                    session.execute(statement + ';')