from nogaspi.views.user.getMyInfos import getMyInfos
from test.functionalTest.dbMagement import sqlQuerysWithCommit
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_user_getMyInfos():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    funcRtr = getMyInfos(FakeRequest({"token":"token_toto"}))

    assert type(funcRtr) == dict

def test_user_getMyInfos_if_bad_token():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        getMyInfos(FakeRequest({"token":"token_tata"}))

def test_user_getMyInfos_if_expired_token():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() - INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        getMyInfos(FakeRequest({"token":"token_toto"}))