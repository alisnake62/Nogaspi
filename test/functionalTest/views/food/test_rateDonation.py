from nogaspi.views.food.rateDonation import rateDonation
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_food_rateDonation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idUserTaker`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '2', '1');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idUserTaker`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '2', '1');"
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = rateDonation(FakeRequest({"token":"token_tata", "idDonation": 1, "note": 4}))
    funcRtr = rateDonation(FakeRequest({"token":"token_tata", "idDonation": 2, "note": 2}))
    assert funcRtr["isRated"]
    assert sqlSelect(table="donation", conditions="WHERE id = 1")[0]['rating'] == 4
    assert sqlSelect(table="donation", conditions="WHERE id = 2")[0]['rating'] == 2
    assert sqlSelect(table="donation", conditions="WHERE id = 1")[0]['idUserTaker'] == 2
    assert sqlSelect(table="donation", conditions="WHERE id = 2")[0]['idUserTaker'] == 2
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['rating'] == 3.0
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['ratingCount'] == 2

def test_food_rateDonation_with_one_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idUserTaker`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '2', '1');",
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = rateDonation(FakeRequest({"token":"token_tata", "idDonation": 1, "note": 4}))
    assert funcRtr["isRated"]
    assert sqlSelect(table="donation", conditions="WHERE id = 1")[0]['rating'] == 4
    assert sqlSelect(table="donation", conditions="WHERE id = 1")[0]['idUserTaker'] == 2
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['rating'] == 4.0
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['ratingCount'] == 1

def test_food_rateDonation_with_expired_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idUserTaker`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, '2', '1');",
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = rateDonation(FakeRequest({"token":"token_tata", "idDonation": 1, "note": 4}))
    assert funcRtr["isRated"]
    assert sqlSelect(table="donation", conditions="WHERE id = 1")[0]['rating'] == 4
    assert sqlSelect(table="donation", conditions="WHERE id = 1")[0]['idUserTaker'] == 2
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['rating'] == 4.0
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['ratingCount'] == 1

def test_food_rateDonation_not_archived_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idUserTaker`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '2', '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idUserTaker`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '2', '1');"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        rateDonation(FakeRequest({"token":"token_tata", "idDonation": 1, "note": 4}))

def test_food_rateDonation_my_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idUserTaker`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '2', '1');",
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        rateDonation(FakeRequest({"token":"token_toto", "idDonation": 1, "note": 4}))

def test_food_rateDonation_id_Iam_not_taker():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idUserTaker`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '2', '1');",
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        rateDonation(FakeRequest({"token":"token_titi", "idDonation": 1, "note": 4}))

def test_food_rateDonation_already_rated():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `rating`, `idUserTaker`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '3', '2', '1');",
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        rateDonation(FakeRequest({"token":"token_tata", "idDonation": 1, "note": 4}))