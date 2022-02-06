from nogaspi.views.register.login import login
from test.functionalTest.dbMagement import sqlQuerysWithCommit
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_register_login():
    sqlQuerysWithCommit([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, NOW(), NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    inputRequest = {
    "mail":"toto@toto.fr",
    "password":"toto"
    }
    funcRtr = login(FakeRequest(inputRequest))
    
    assert len(funcRtr['token']) == 64
    assert 'token_expiration' in funcRtr

def test_register_login_with_bad_password():
    sqlQuerysWithCommit([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, NOW(), NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    inputRequest = {
    "mail":"toto@toto.fr",
    "password":"tata"
    }
    with pytest.raises(Exception):
        login(FakeRequest(inputRequest))

def test_register_login_with_bad_user():
    sqlQuerysWithCommit([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, NOW(), NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    inputRequest = {
    "mail":"toto@tata.fr",
    "password":"toto"
    }
    with pytest.raises(Exception):
        login(FakeRequest(inputRequest))
