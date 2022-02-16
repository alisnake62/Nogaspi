from nogaspi.views.user.postFireBaseToken import postFireBaseToken
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_user_postFireBaseToken():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, 'fireBase_token_toto');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, 'fireBase_token_titi');"
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = postFireBaseToken(FakeRequest({
        "token":"token_toto",
        "fireBaseToken": "fireBase_token_toto"
    }))

    assert funcRtr['isPosted']
    assert sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['fireBaseToken'] == "fireBase_token_toto"
    assert sqlSelect(table='userNogaspi', conditions="WHERE id = 2")[0]['fireBaseToken'] == None    # Delete this FBToken for other User
    assert sqlSelect(table='userNogaspi', conditions="WHERE id = 3")[0]['fireBaseToken'] == "fireBase_token_titi"   # Check if this FBToken if already in DB

def test_user_postFireBaseToken_with_bas_user():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        postFireBaseToken(FakeRequest({
            "token":"token_tata",
            "fireBaseToken": "fireBase_token_toto"
        }))

def test_user_postFireBaseToken_with_user_not_login():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() - INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        postFireBaseToken(FakeRequest({
            "token":"token_toto",
            "fireBaseToken": "fireBase_token_toto"
        }))