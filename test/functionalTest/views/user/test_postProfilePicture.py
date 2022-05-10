from nogaspi.views.user.postProfilePicture import postProfilePicture
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest, generateAndSaveFile
import pytest
import os

def test_user_postProfilePicture():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    funcRtr = postProfilePicture(FakeRequest({"token": "token_toto"}, files={"profilePicture": 'totoFile.jpg'}))

    assert os.path.isfile(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.jpg")
    os.remove(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.jpg")
    assert funcRtr['isPosted']
    assert sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['profilePicture'] == "toto.jpg"


def test_user_postProfilePicture_if_file_already_exist():
    generateAndSaveFile(f"{os.environ['DIRECTORY_ASSET']}images/users/", "toto.png")
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', 'toto.png', 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    assert os.path.isfile(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.png")

    funcRtr = postProfilePicture(FakeRequest({"token": "token_toto"}, files={"profilePicture": 'totoFile.jpg'}))

    assert not os.path.isfile(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.png")
    assert os.path.isfile(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.jpg")
    os.remove(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.jpg")
    assert funcRtr['isPosted']
    assert sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['profilePicture'] == "toto.jpg"

    if os.path.isfile(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.png"):
        os.remove(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.png")

def test_user_postProfilePicture_if_file_already_exist_on_in_db():
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', 'toto.png', 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL, NULL);"]
    sqlQuerysWithCommit(querys)

    assert not os.path.isfile(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.png")

    funcRtr = postProfilePicture(FakeRequest({"token": "token_toto"}, files={"profilePicture": 'totoFile.jpg'}))

    assert os.path.isfile(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.jpg")
    os.remove(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.jpg")
    assert funcRtr['isPosted']
    assert sqlSelect(table='userNogaspi', conditions="WHERE id = 1")[0]['profilePicture'] == "toto.jpg"

    if os.path.isfile(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.png"):
        os.remove(f"{os.environ['DIRECTORY_ASSET']}images/users/toto.png")
