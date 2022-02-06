from nogaspi.views.food.deleteArticlesInFridge import deleteArticlesInFridge
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_food_deleteArticlesInFridge():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)
    assert sqlSelect(table='article', conditions='WHERE id = 1')[0]['idFridge'] == 1
    assert sqlSelect(table='article', conditions='WHERE id = 2')[0]['idFridge'] == 1
    
    funcRtr = deleteArticlesInFridge(FakeRequest({"token":"token_toto", "idArticles": [1, 2]}))
    
    assert funcRtr['isDelete (Remove from fridge)']
    assert sqlSelect(table='article', conditions='WHERE id = 1')[0]['idFridge'] is None
    assert sqlSelect(table='article', conditions='WHERE id = 2')[0]['idFridge'] is None

def test_food_deleteArticlesInFridge_with_one_article():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)
    assert sqlSelect(table='article', conditions='WHERE id = 1')[0]['idFridge']
    
    funcRtr = deleteArticlesInFridge(FakeRequest({"token":"token_toto", "idArticles": [1]}))
    
    assert funcRtr['isDelete (Remove from fridge)']
    assert sqlSelect(table='article', conditions='WHERE id = 1')[0]['idFridge'] is None

def test_food_deleteArticlesInFridge_with_bad_articles():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        deleteArticlesInFridge(FakeRequest({"token":"token_toto", "idArticles": [2]}))

def test_food_deleteArticlesInFridge_if_article_is_not_in_my_fridge():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, NULL);"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        deleteArticlesInFridge(FakeRequest({"token":"token_toto", "idArticles": [1]}))

def test_food_deleteArticlesInFridge_if_article_is_in_valid_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('1', '1', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        deleteArticlesInFridge(FakeRequest({"token":"token_toto", "idArticles": [1]}))

def test_food_deleteArticlesInFridge_if_in_expired_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('1', '1', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)
    assert sqlSelect(table='article', conditions='WHERE id = 1')[0]['idFridge'] == 1
    
    funcRtr = deleteArticlesInFridge(FakeRequest({"token":"token_toto", "idArticles": [1]}))
    
    assert funcRtr['isDelete (Remove from fridge)']
    assert sqlSelect(table='article', conditions='WHERE id = 1')[0]['idFridge'] is None

def test_food_deleteArticlesInFridge_if_in_archived_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `idDonation`, `expirationDate`, `idFridge`) VALUES ('1', '1', '1', NOW() + INTERVAL 1 DAY, '1');"
    ]
    sqlQuerysWithCommit(querys)
    assert sqlSelect(table='article', conditions='WHERE id = 1')[0]['idFridge'] == 1
    
    funcRtr = deleteArticlesInFridge(FakeRequest({"token":"token_toto", "idArticles": [1]}))
    
    assert funcRtr['isDelete (Remove from fridge)']
    assert sqlSelect(table='article', conditions='WHERE id = 1')[0]['idFridge'] is None
