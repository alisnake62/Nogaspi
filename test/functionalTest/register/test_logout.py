from nogaspi.views.register.logout import logout
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_register_logout():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, 'firebase_totken_toto');"]
    sqlQuerysWithCommit(querys)

    funcRtr = logout(FakeRequest({"token": 'token_toto'}))
    assert funcRtr['logout']
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['token'] == None
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['token_expiration'] == None
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['fireBaseToken'] == None

def test_register_logout_with_token_already_expired():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() - INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, 'firebase_totken_toto');"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        logout(FakeRequest({"token": 'token_toto'}))