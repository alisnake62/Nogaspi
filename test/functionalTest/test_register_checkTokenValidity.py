from nogaspi.views.register.checkTokenValidity import checkTokenValidityTest
from test.functionalTest.dbMagement import sqlQuery, DBTestLifeCicle
import datetime

def test_register_checkTokenValidity():
    with DBTestLifeCicle():
        timeAfterNow = datetime.datetime.now() + datetime.timedelta(minutes = 15)
        sqlQuery(f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (NULL, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);")
        fnrtr = checkTokenValidityTest("token_toto")

    assert fnrtr['validity']
    assert fnrtr['user'] == 'toto@toto.fr'

def test_register_checkTokenValidity_with_bad_Token():
    with DBTestLifeCicle():
        timeAfterNow = datetime.datetime.now() + datetime.timedelta(minutes = 15)
        sqlQuery(f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (NULL, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);")
        fnrtr = checkTokenValidityTest("token_tata")

    assert fnrtr == {'validity': False, 'user' : 'Unknown', 'token_expiration': 'Unknown'}
    
def test_register_checkTokenValidity_with_bad_expirationDate():
    with DBTestLifeCicle():
        timeAfterNow = datetime.datetime.now() - datetime.timedelta(minutes = 15)
        sqlQuery(f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (NULL, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);")
        fnrtr = checkTokenValidityTest("token_toto")

    assert not fnrtr['validity']
    assert fnrtr['user'] == 'toto@toto.fr'