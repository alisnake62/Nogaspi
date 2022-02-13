from nogaspi.views.food.getByBarCode import getByBarCode
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest

import pytest

def test_food_getByBarCode():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getByBarCode(FakeRequest({"token":"token_toto", "barcode": "3267110001144"}))
    assert funcRtr['name'] == "Purée Noix de Cajou"
    assert len (sqlSelect(table="product")) == 1
    assert sqlSelect(table="product")[0]["barcode"] == "3267110001144"
    assert sqlSelect(table="product")[0]["name"] == "Purée Noix de Cajou"

def test_food_getByBarCode_with_barcode_already_in_db():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `product` (`id`, `barcode`, `name`, `idLastScanUser`, `lastScanDate`) VALUES (1, '3267110001144', 'nameTest', '1', NOW())",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getByBarCode(FakeRequest({"token":"token_toto", "barcode": "3267110001144"}))
    assert funcRtr['name'] == "nameTest"
    assert len (sqlSelect(table="product")) == 1
    assert sqlSelect(table="product")[0]["barcode"] == "3267110001144"
    assert sqlSelect(table="product")[0]["name"] == "nameTest"

def test_food_getByBarCode_with_barcode_already_in_db():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `product` (`id`, `barcode`, `name`, `idLastScanUser`, `lastScanDate`) VALUES (1, '3267110001144', 'nameTest', '1', NOW())",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getByBarCode(FakeRequest({"token":"token_toto", "barcode": "3267110001144"}))
    assert funcRtr['name'] == "nameTest"
    assert len (sqlSelect(table="product")) == 1
    assert sqlSelect(table="product")[0]["barcode"] == "3267110001144"
    assert sqlSelect(table="product")[0]["name"] == "nameTest"

def test_food_getByBarCode_with_bad_barcode():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        getByBarCode(FakeRequest({"token":"token_toto", "barcode": "010101"}))
    assert len (sqlSelect(table="product")) == 0