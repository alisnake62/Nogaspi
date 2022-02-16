from nogaspi.views.food.getDonationById import getDonationById
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_food_getDonationById():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getDonationById(FakeRequest({
        "token":"token_toto",
        "idDonation": 1
    }))
    assert funcRtr["donation"]["id"] == 1

def test_food_getDonationById_with_expired_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '43.6', '1.5', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getDonationById(FakeRequest({
        "token":"token_toto",
        "idDonation": 1
    }))
    assert funcRtr["donation"]["id"] == 1

def test_food_getDonationById_with_archived_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '1');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getDonationById(FakeRequest({
        "token":"token_toto",
        "idDonation": 1
    }))
    assert funcRtr["donation"]["id"] == 1

def test_food_getDonationById_with_bad_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '1');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        getDonationById(FakeRequest({
        "token":"token_toto",
        "idDonation": 2
    }))