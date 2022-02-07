from nogaspi.views.food.getArticlesInFridge import getArticlesInFridge
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest

def test_food_getArticlesInFridge():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('2', '2'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '2');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('3', '1', NOW() + INTERVAL 1 DAY, '1');",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getArticlesInFridge(FakeRequest({"token":"token_toto"}))
    assert [a['id'] for a in funcRtr['articles']] == [1, 3]

def test_food_getArticlesInFridge_with_empty_list():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); "
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getArticlesInFridge(FakeRequest({"token":"token_toto"}))
    assert funcRtr['articles'] == []

def test_food_getArticlesInFridge_with_expired_article():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('2', '2'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '2');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('3', '1', NOW() - INTERVAL 1 DAY, '1');",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getArticlesInFridge(FakeRequest({"token":"token_toto"}))
    assert [a['id'] for a in funcRtr['articles']] == [1, 3]

def test_food_getArticlesInFridge_with_expired_article_more_than_15_days():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('2', '2'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '101010', '1', NOW())",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('1', '1', NOW() + INTERVAL 1 DAY, '1');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('2', '1', NOW() + INTERVAL 1 DAY, '2');",
        "INSERT INTO `article` (`id`, `idProduct`, `expirationDate`, `idFridge`) VALUES ('3', '1', NOW() - INTERVAL 20 DAY, '1');",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getArticlesInFridge(FakeRequest({"token":"token_toto"}))
    assert [a['id'] for a in funcRtr['articles']] == [1]