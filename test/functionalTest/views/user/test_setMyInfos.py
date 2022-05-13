from nogaspi.views.user.setMyInfos import setMyInfos
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_user_setMyInfos():
    querys = [
        "INSERT INTO `allergen` (`id`, `nameEN`, `nameFR`) VALUES (1, 'peanuts', 'cacahuete');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `address`, `idAllergen`, `favoriteDistanceToSearch`, `favoriteGeoPrecisionToDonate`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL);"
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = setMyInfos(FakeRequest({
        "token":"token_toto",
        "address": "1 avenue du chapeau 66666 Chaussette",
        "idAllergen": 1,
        "favoriteDistanceToSearch": 500,
        "favoriteGeoPrecisionToDonate": 300
    }))

    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['address'] == "1 avenue du chapeau 66666 Chaussette"
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['idAllergen'] == 1
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['favoriteDistanceToSearch'] == 500
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['favoriteGeoPrecisionToDonate'] == 300

def test_user_setMyInfos_with_modifiy_values():
    querys = [
        "INSERT INTO `allergen` (`id`, `nameEN`, `nameFR`) VALUES (1, 'peanuts', 'cacahuete');",
        "INSERT INTO `allergen` (`id`, `nameEN`, `nameFR`) VALUES (2, 'milk', 'lait');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `address`, `idAllergen`, `favoriteDistanceToSearch`, `favoriteGeoPrecisionToDonate`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', 'fake address', 2, 200, 100);"
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = setMyInfos(FakeRequest({
        "token":"token_toto",
        "address": "1 avenue du chapeau 66666 Chaussette",
        "idAllergen": 1,
        "favoriteDistanceToSearch": 500,
        "favoriteGeoPrecisionToDonate": 300
    }))

    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['address'] == "1 avenue du chapeau 66666 Chaussette"
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['idAllergen'] == 1
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['favoriteDistanceToSearch'] == 500
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['favoriteGeoPrecisionToDonate'] == 300

def test_user_setMyInfos_with_modifiy_None_Value():
    querys = [
        "INSERT INTO `allergen` (`id`, `nameEN`, `nameFR`) VALUES (1, 'peanuts', 'cacahuete');",
        "INSERT INTO `allergen` (`id`, `nameEN`, `nameFR`) VALUES (2, 'milk', 'lait');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `address`, `idAllergen`, `favoriteDistanceToSearch`, `favoriteGeoPrecisionToDonate`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', 'fake address', 2, 200, 100);"
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = setMyInfos(FakeRequest({
        "token":"token_toto",
        "address": None,
        "idAllergen": 1,
        "favoriteDistanceToSearch": None,
        "favoriteGeoPrecisionToDonate": 300
    }))

    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['address'] == None
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['idAllergen'] == 1
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['favoriteDistanceToSearch'] == None
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['favoriteGeoPrecisionToDonate'] == 300

def test_user_setMyInfos_with_bad_allergen_id():
    querys = [
        "INSERT INTO `allergen` (`id`, `nameEN`, `nameFR`) VALUES (1, 'peanuts', 'cacahuete');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`, `address`, `idAllergen`, `favoriteDistanceToSearch`, `favoriteGeoPrecisionToDonate`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0', NULL, NULL, NULL, NULL);"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        setMyInfos(FakeRequest({
            "token":"token_toto",
            "address": "1 avenue du chapeau 66666 Chaussette",
            "idAllergen": 2,
            "favoriteDistanceToSearch": 500,
            "favoriteGeoPrecisionToDonate": 300
        }))