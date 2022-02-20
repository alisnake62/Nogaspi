from nogaspi.views.food.takeDonations import takeDonations
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_food_takeDonations():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donationCode` (`id`, `code`, `expirationDate`) VALUES (1, 'ABCDEF', NOW() + INTERVAL 1 DAY)",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '1', '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '1', '0');",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('1', '1', '1', NOW() + INTERVAL 1 DAY, NULL);",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (2, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('2', '1', '1', NOW() + INTERVAL 1 DAY, NULL);",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (3, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('3', '1', '2', NOW() + INTERVAL 1 DAY, NULL);"
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = takeDonations(FakeRequest({"token":"token_tata", "donationCode": "ABCDEF"}))
    assert funcRtr["isTaked"]
    assert sqlSelect(table="donation", conditions="WHERE id = 1")[0]['archive'] == 1
    assert sqlSelect(table="donation", conditions="WHERE id = 2")[0]['archive'] == 1
    assert sqlSelect(table="donation", conditions="WHERE id = 1")[0]['idUserTaker'] == 2
    assert sqlSelect(table="donation", conditions="WHERE id = 2")[0]['idUserTaker'] == 2
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['points'] == 12
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 2")[0]['points'] == 3

def test_food_takeDonations_with_expired_code():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donationCode` (`id`, `code`, `expirationDate`) VALUES (1, 'ABCDEF', NOW() - INTERVAL 1 DAY)",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '1', '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '1', '0');",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('1', '1', '1', NOW() + INTERVAL 1 DAY, NULL);",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (2, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('2', '1', '1', NOW() + INTERVAL 1 DAY, NULL);",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (3, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('3', '1', '2', NOW() + INTERVAL 1 DAY, NULL);"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        takeDonations(FakeRequest({"token":"token_tata", "donationCode": "ABCDEF"}))

def test_food_takeDonations_with_my_donationCode():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donationCode` (`id`, `code`, `expirationDate`) VALUES (1, 'ABCDEF', NOW() + INTERVAL 1 DAY)",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '1', '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '1', '0');",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('1', '1', '1', NOW() + INTERVAL 1 DAY, NULL);",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (2, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('2', '1', '1', NOW() + INTERVAL 1 DAY, NULL);",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (3, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('3', '1', '2', NOW() + INTERVAL 1 DAY, NULL);"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        takeDonations(FakeRequest({"token":"token_toto", "donationCode": "ABCDEF"}))

def test_food_takeDonations_with_bad_donationCode():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donationCode` (`id`, `code`, `expirationDate`) VALUES (1, 'ABCDEF', NOW() + INTERVAL 1 DAY)",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '1', '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, '1', '0');",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('1', '1', '1', NOW() + INTERVAL 1 DAY, NULL);",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (2, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('2', '1', '1', NOW() + INTERVAL 1 DAY, NULL);",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (3, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('3', '1', '2', NOW() + INTERVAL 1 DAY, NULL);"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        takeDonations(FakeRequest({"token":"token_tata", "donationCode": "ABCDEG"}))
    