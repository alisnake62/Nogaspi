from nogaspi.views.register.checkTokenValidity import checkTokenValidityTest
from nogaspi.dbEngine import EngineSQLAlchemy

def test_register_checkTokenValidity():

    with EngineSQLAlchemy() as session:
        session.execute("DROP DATABASE IF EXISTS `nogaspi`;")
        with open("test/nogaspi.sql", encoding="utf-8") as sql_file:
            for statement in sql_file.read().split(';'):
                if len(statement.strip()) > 0:
                    session.execute(statement + ';')
        session.commit()

    with EngineSQLAlchemy() as session:
        session.execute("INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (NULL, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '2022-02-02 19:26:32.000000', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);")
        session.commit()
    test = checkTokenValidityTest("token_toto")
    assert test['validity'] == False