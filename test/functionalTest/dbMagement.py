from nogaspi.dbEngine import EngineSQLAlchemy

class DBTestLifeCicle:

    def __enter__(self):
        with EngineSQLAlchemy() as session:
            session.execute("DROP DATABASE IF EXISTS `nogaspi`;")
            with open("test/nogaspi.sql", encoding="utf-8") as sql_file:
                for statement in sql_file.read().split(';'):
                    if len(statement.strip()) > 0:
                        session.execute(statement + ';')
            session.commit()

    def __exit__(self, type, value, traceback):
        with EngineSQLAlchemy() as session:
            session.execute("DROP DATABASE IF EXISTS `nogaspi`;")
            session.execute("CREATE DATABASE IF NOT EXISTS `nogaspi` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci;")

def sqlQuery(query):
    with EngineSQLAlchemy() as session:
        session.execute(query)
        session.commit()