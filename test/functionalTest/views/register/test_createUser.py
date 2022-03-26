import datetime
from nogaspi.views.register.createUser import createUser
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_register_createUser():

    assert len(sqlSelect(table="userNogaspi")) == 0

    funcRtr = createUser(FakeRequest({
        "mail":"clementsergent@yahoo.fr",
        "password":"password",
        "pseudo":"ClementTest"
    }))
    
    assert funcRtr['userCreateConfirmationCodeAsk']
    assert len(sqlSelect(table="userNogaspi")) == 1
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['token'] == None
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['password'] == "password"
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['pseudo'] == "ClementTest"
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['isConfirmate'] == 0
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['points'] == 0
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['rating'] == 0
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['fireBaseToken'] == None
    assert len(sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['confirmationCode']) == 10
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['confirmationCodeExpiration'] > datetime.datetime.now() + datetime.timedelta(minutes = 9)
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['confirmationCodeExpiration'] < datetime.datetime.now() + datetime.timedelta(minutes = 10)

def test_register_createUser_if_user_already_exist():
    
    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`, `isConfirmate`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, NOW(), NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL, '1');"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        createUser(FakeRequest({
            "mail":"toto@toto.fr",
            "password":"password",
            "pseudo":"toto"
        }))

def test_register_createUser_if_user_already_exist_but_not_confirmate():

    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`, `confirmationCode`, `confirmationCodeExpiration`) VALUES (1, 'clementsergent@yahoo.fr', 'toto', 'toto', '0', '1234567890', NOW() + INTERVAL 5 MINUTE);"]
    sqlQuerysWithCommit(querys)

    assert len(sqlSelect(table="userNogaspi")) == 1

    currentCode = sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['confirmationCode']
    currentExpirationDate = sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['confirmationCodeExpiration']

    funcRtr = createUser(FakeRequest({
        "mail":"clementsergent@yahoo.fr",
        "password":"password",
        "pseudo":"ClementTest2"
    }))
    
    assert funcRtr['userCreateConfirmationCodeAsk']
    assert len(sqlSelect(table="userNogaspi")) == 1
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['token'] == None
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['password'] == "password"
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['pseudo'] == "ClementTest2"
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['isConfirmate'] == 0
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['points'] == 0
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['rating'] == 0
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['fireBaseToken'] == None
    assert len(sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['confirmationCode']) == 10
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['confirmationCode'] != currentCode
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['confirmationCodeExpiration'] > datetime.datetime.now() + datetime.timedelta(minutes = 9)
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['confirmationCodeExpiration'] != currentExpirationDate

def test_register_createUser_if_pseudo_already_used():

    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`) VALUES (1, 'toto@toto.fr', 'toto', 'ClementTest', '1');"]
    sqlQuerysWithCommit(querys)

    assert len(sqlSelect(table="userNogaspi")) == 1

    with pytest.raises(Exception):
        createUser(FakeRequest({
            "mail":"clementsergent@yahoo.fr",
            "password":"password",
            "pseudo":"ClementTest"
        }))

def test_register_createUser_if_pseudo_already_used_but_not_confirmate():

    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`) VALUES (1, 'toto@toto.fr', 'toto', 'ClementTest', '0');"]
    sqlQuerysWithCommit(querys)

    assert len(sqlSelect(table="userNogaspi")) == 1

    funcRtr = createUser(FakeRequest({
        "mail":"clementsergent@yahoo.fr",
        "password":"password",
        "pseudo":"ClementTest"
    }))
    
    assert funcRtr['userCreateConfirmationCodeAsk']
    assert len(sqlSelect(table="userNogaspi")) == 2
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['id'] != 1
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['token'] == None
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['password'] == "password"
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['pseudo'] == "ClementTest"
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['isConfirmate'] == 0
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['points'] == 0
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['rating'] == 0
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['fireBaseToken'] == None
    assert len(sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['confirmationCode']) == 10
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['confirmationCodeExpiration'] > datetime.datetime.now() + datetime.timedelta(minutes = 9)
    assert sqlSelect(table="userNogaspi", conditions="WHERE mail = 'clementsergent@yahoo.fr'")[0]['confirmationCodeExpiration'] < datetime.datetime.now() + datetime.timedelta(minutes = 10)

def test_register_createUser_if_pseudo_already_exist_with_not_confirmate_and_confirmate():

    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`) VALUES (1, 'clementsergent@yahoo.fr', 'toto', 'toto', '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`) VALUES (2, 'clementsergent@yahoo.fr', 'toto', 'toto', '1');"
    ]
    sqlQuerysWithCommit(querys)

    assert len(sqlSelect(table="userNogaspi")) == 2

    with pytest.raises(Exception):
        createUser(FakeRequest({
            "mail":"toto@toto.fr",
            "password":"password",
            "pseudo":"toto"
        }))