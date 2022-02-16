from nogaspi.views.user.postRegularPath import postRegularPath
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest


'token',
'latitudeStart',
'longitudeStart',
'latitudeEnd',
'longitudeEnd',
'pathPoints'

def test_user_postRegularPath():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    funcRtr = postRegularPath(FakeRequest({
        "token":"token_toto",
        "latitudeStart": 44.5,
        "longitudeStart": 1.5,
        "latitudeEnd": 44.6,
        "longitudeEnd": 1.6,
        "pathPoints": [
            {
                "latitude": 44.54,
                "longitude":1.54
            },
            {
                "latitude": 44.58,
                "longitude":1.58
            }
        ]
    }))

    assert funcRtr['isPosted']
    assert sqlSelect(table="userNogaspi")[0]["regularPathLatitudeStart"] == 44.5
    assert sqlSelect(table="userNogaspi")[0]["regularPathLongitudeStart"] == 1.5
    assert sqlSelect(table="userNogaspi")[0]["regularPathLatitudeEnd"] == 44.6
    assert sqlSelect(table="userNogaspi")[0]["regularPathLongitudeEnd"] == 1.6
    assert sqlSelect(table="userNogaspi")[0]["regularPathPoints"] == b'"[{\\"latitude\\": 44.54, \\"longitude\\": 1.54}, {\\"latitude\\": 44.58, \\"longitude\\": 1.58}]"'

def test_user_postRegularPath_with_bad_user():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        postRegularPath(FakeRequest({
            "token":"tokena_tata",
            "latitudeStart": 44.5,
            "longitudeStart": 1.5,
            "latitudeEnd": 44.6,
            "longitudeEnd": 1.6,
            "pathPoints": [
                {
                    "latitude": 44.54,
                    "longitude":1.54
                },
                {
                    "latitude": 44.58,
                    "longitude":1.58
                }
            ]
        }))