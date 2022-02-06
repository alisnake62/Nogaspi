from nogaspi.views.register.checkTokenValidity import checkTokenValidity
from test.functionalTest.dbMagement import sqlQuery
from test.functionalTest.flaskManagement import FakeRequest
import datetime

def test_register_checkTokenValidity():
    timeAfterNow = datetime.datetime.now() + datetime.timedelta(minutes = 15)
    sqlQuery([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    funcRtr = checkTokenValidity(FakeRequest({"token":"token_toto"}))
    
    assert funcRtr['validity']
    assert funcRtr['user'] == 'toto@toto.fr'


def test_register_checkTokenValidity_with_bad_Token():
    timeAfterNow = datetime.datetime.now() + datetime.timedelta(minutes = 15)
    sqlQuery([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    funcRtr = checkTokenValidity(FakeRequest({"token":"token_titi"}))

    assert funcRtr == {'validity': False, 'user' : 'Unknown', 'token_expiration': 'Unknown'}

def test_register_checkTokenValidity_with_bad_expirationDate():
    timeAfterNow = datetime.datetime.now() - datetime.timedelta(minutes = 15)
    sqlQuery([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    funcRtr = checkTokenValidity(FakeRequest({"token":"token_toto"}))

    assert not funcRtr['validity']
    assert funcRtr['user'] == 'toto@toto.fr'
