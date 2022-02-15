from nogaspi.views.user.getRegularPath import getRegularPath
from test.functionalTest.dbMagement import sqlQuerysWithCommit
from test.functionalTest.flaskManagement import FakeRequest
import pytest

regularPathPoints = "[{\\\\\\\"latitude\\\\\\\": 43.58446, \\\\\\\"longitude\\\\\\\": 1.46247}, {\\\\\\\"latitude\\\\\\\": 43.58444, \\\\\\\"longitude\\\\\\\": 1.46245}]"

def test_user_getRegularPath():
    querys = [
        f"INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', 43.5844, 1.4626, 43.6108, 1.41365, '\\\"{regularPathPoints}\\\"');"
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = getRegularPath(FakeRequest({"token":"token_toto"}))

    assert funcRtr['regularPath'] == {
        'latitudeStart': 43.5844,
        'longitudeStart': 1.4626,
        'latitudeEnd': 43.6108,
        'longitudeEnd': 1.41365,
        'pathPoints': [
            {
                "latitude": 43.58446,
                "longitude": 1.46247
            },
            {
                "latitude": 43.58444,
                "longitude": 1.46245
            }
        ]
    }

def test_user_getRegularPath_with_not_regularPath():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', 43.5844, 1.4626, 43.6108, 1.41365, NULL);"
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = getRegularPath(FakeRequest({"token":"token_toto"}))

    assert funcRtr['regularPath'] == {
        'latitudeStart': 43.5844,
        'longitudeStart': 1.4626,
        'latitudeEnd': 43.6108,
        'longitudeEnd': 1.41365,
        'pathPoints': None
    }


def test_user_getRegularPath_with_bad_user():
    querys = [
        f"INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', 43.5844, 1.4626, 43.6108, 1.41365, '\\\"{regularPathPoints}\\\"');"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        getRegularPath(FakeRequest({"token":"token_tata"}))
