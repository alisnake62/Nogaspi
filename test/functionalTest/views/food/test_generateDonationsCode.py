from nogaspi.views.food.generateDonationsCode import generateDonationsCode
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest
import datetime

def test_food_generateDonationsCode():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = generateDonationsCode(FakeRequest({"token":"token_toto", "idDonations": [1,2]}))
    assert len(funcRtr["code"]) == 64
    assert sqlSelect(table='donationCode')[0]['code'] == funcRtr["code"]
    assert sqlSelect(table='donation', conditions='WHERE id = 1')[0]['idDonationCode'] == sqlSelect(table='donationCode')[0]['id']
    assert sqlSelect(table='donation', conditions='WHERE id = 2')[0]['idDonationCode'] == sqlSelect(table='donationCode')[0]['id']
    assert sqlSelect(table='donationCode')[0]['expirationDate'] > datetime.datetime.now() + datetime.timedelta(minutes = 4)
    assert sqlSelect(table='donationCode')[0]['expirationDate'] < datetime.datetime.now() + datetime.timedelta(minutes = 6)

def test_food_generateDonationsCode_with_one_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = generateDonationsCode(FakeRequest({"token":"token_toto", "idDonations": [1]}))
    assert len(funcRtr["code"]) == 64
    assert sqlSelect(table='donationCode')[0]['code'] == funcRtr["code"]
    assert sqlSelect(table='donation', conditions='WHERE id = 1')[0]['idDonationCode'] == sqlSelect(table='donationCode')[0]['id']
    assert sqlSelect(table='donationCode')[0]['expirationDate'] > datetime.datetime.now()
    assert sqlSelect(table='donationCode')[0]['expirationDate'] < datetime.datetime.now() + datetime.timedelta(minutes = 6)

def test_food_generateDonationsCode_with_bad_donations():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        generateDonationsCode(FakeRequest({"token":"token_toto", "idDonations": [1,3]}))
    assert len(sqlSelect(table='donationCode')) == 0

def test_food_generateDonationsCode_with_not_my_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '2', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        generateDonationsCode(FakeRequest({"token":"token_toto", "idDonations": [1,2]}))
    assert len(sqlSelect(table='donationCode')) == 0

def test_food_generateDonationsCode_with_expired_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '0');",
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        generateDonationsCode(FakeRequest({"token":"token_toto", "idDonations": [1,2]}))
    assert len(sqlSelect(table='donationCode')) == 0

def test_food_generateDonationsCode_with_archived_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '1');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        generateDonationsCode(FakeRequest({"token":"token_toto", "idDonations": [1,2]}))
    assert len(sqlSelect(table='donationCode')) == 0