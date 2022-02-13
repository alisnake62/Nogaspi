from nogaspi.views.food.postDonationFromFridge import postDonationFromFridge
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest
import datetime

def test_food_postDonationFromFridge():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() - INTERVAL 10 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('3', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = postDonationFromFridge(FakeRequest({
        "token": "token_toto",
        "articles": [{"id": 1}, {"id": 2}],
        "latitude": 43.5,
        "longitude": 1.5,
        "geoPrecision": 500,
        "endingDate": str(datetime.date.today() + datetime.timedelta(days=10))
    }))
    assert funcRtr['isPosted']
    assert len(sqlSelect(table='donation')) == 1
    assert sqlSelect(table='article', conditions="WHERE id = 1")[0]['idDonation'] == sqlSelect(table='donation')[0]['id']
    assert sqlSelect(table='article', conditions="WHERE id = 2")[0]['idDonation'] == sqlSelect(table='donation')[0]['id']
    assert sqlSelect(table='article', conditions="WHERE id = 3")[0]['idDonation'] is None
    assert sqlSelect(table='donation')[0]["latitude"] == 43.5
    assert sqlSelect(table='donation')[0]["longitude"] == 1.5
    assert sqlSelect(table='donation')[0]["geoPrecision"] == 500

def test_food_postDonationFromFridge_bad_user():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('2', '2');",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('3', '1', NOW() + INTERVAL 1 DAY, '2');"
    ]
    sqlQuerysWithCommit(querys)
    with pytest.raises(Exception):
        postDonationFromFridge(FakeRequest({
            "token": "token_tata",
            "articles": [{"id": 1}, {"id": 2}],
            "latitude": 43.5,
            "longitude": 1.5,
            "geoPrecision": 500,
            "endingDate": str(datetime.date.today() + datetime.timedelta(days=10))
        }))

def test_food_postDonationFromFridge_with_expire_article():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1');",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() - INTERVAL 20 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('3', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)
    with pytest.raises(Exception):
        postDonationFromFridge(FakeRequest({
            "token": "token_toto",
            "articles": [{"id": 1}, {"id": 2}],
            "latitude": 43.5,
            "longitude": 1.5,
            "geoPrecision": 500,
            "endingDate": str(datetime.date.today() + datetime.timedelta(days=10))
        }))

def test_food_postDonationFromFridge_article_already_in_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`, `idDonation`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1', '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('3', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)
    with pytest.raises(Exception):
        postDonationFromFridge(FakeRequest({
            "token": "token_toto",
            "articles": [{"id": 1}, {"id": 2}],
            "latitude": 43.5,
            "longitude": 1.5,
            "geoPrecision": 500,
            "endingDate": str(datetime.date.today() + datetime.timedelta(days=10))
        }))

def test_food_postDonationFromFridge_with_bad_fridge():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('2', '2');",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('3', '1', NOW() + INTERVAL 1 DAY, '2');"
    ]
    sqlQuerysWithCommit(querys)
    with pytest.raises(Exception):
        postDonationFromFridge(FakeRequest({
            "token": "token_toto",
            "articles": [{"id": 1}, {"id": 3}],
            "latitude": 43.5,
            "longitude": 1.5,
            "geoPrecision": 500,
            "endingDate": str(datetime.date.today() + datetime.timedelta(days=10))
        }))

def test_food_postDonationFromFridge_with_bad_article():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('3', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)
    with pytest.raises(Exception):
        postDonationFromFridge(FakeRequest({
            "token": "token_toto",
            "articles": [{"id": 1}, {"id": 4}],
            "latitude": 43.5,
            "longitude": 1.5,
            "geoPrecision": 500,
            "endingDate": str(datetime.date.today() + datetime.timedelta(days=10))
        }))