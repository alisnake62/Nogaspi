from nogaspi.views.food.deleteMyDonations import deleteMyDonations
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_food_deleteArticlesInFridge():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = deleteMyDonations(FakeRequest({"token":"token_toto", "idDonations": [1, 2]}))
    
    assert funcRtr['isDelete (Archived)']
    assert [d['archive'] for d in sqlSelect(table='donation')] == [1, 1]

def test_food_deleteArticlesInFridge_with_one_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = deleteMyDonations(FakeRequest({"token":"token_toto", "idDonations": [1]}))
    
    assert funcRtr['isDelete (Archived)']
    assert sqlSelect(table='donation', conditions="WHERE id = 1")[0]['archive'] == 1

def test_food_deleteArticlesInFridge_with_bad_donations():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        deleteMyDonations(FakeRequest({"token":"token_toto", "idDonations": [1, 3]}))
    assert [d['archive'] for d in sqlSelect(table='donation')] == [0, 0]

def test_food_deleteArticlesInFridge_with_bad_user():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '2', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        deleteMyDonations(FakeRequest({"token":"token_toto", "idDonations": [1, 2]}))
    assert [d['archive'] for d in sqlSelect(table='donation')] == [0, 0]

def test_food_deleteArticlesInFridge_with_archived_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '1');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        deleteMyDonations(FakeRequest({"token":"token_toto", "idDonations": [1, 2]}))
    assert sqlSelect(table='donation', conditions="WHERE id = 2")[0]['archive'] == 0

def test_food_deleteArticlesInFridge_with_expired_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        deleteMyDonations(FakeRequest({"token":"token_toto", "idDonations": [1, 2]}))
    assert [d['archive'] for d in sqlSelect(table='donation')] == [0, 0]
