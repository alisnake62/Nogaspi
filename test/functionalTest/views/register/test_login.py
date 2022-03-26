from nogaspi.views.register.login import login
from test.functionalTest.dbMagement import sqlQuerysWithCommit
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_register_login():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`, `isConfirmate`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, NOW(), NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL, '1');"]
    sqlQuerysWithCommit(querys)

    funcRtr = login(FakeRequest({
        "mail":"toto@toto.fr",
        "password":"toto"
    }))
    
    assert len(funcRtr['token']) == 64
    assert 'token_expiration' in funcRtr

def test_register_login_with_bad_password():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`, `isConfirmate`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, NOW(), NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL, '1');"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        login(FakeRequest({
            "mail":"toto@toto.fr",
            "password":"tata"
        }))

def test_register_login_with_bad_user():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`, `isConfirmate`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, NOW(), NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL, '1');"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        login(FakeRequest({
            "mail":"toto@tata.fr",
            "password":"toto"
        }))

def test_register_login_with_user_not_confirmate():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`, `isConfirmate`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, NOW(), NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL, '0');"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        login(FakeRequest({
            "mail":"toto@toto.fr",
            "password":"toto"
        }))
