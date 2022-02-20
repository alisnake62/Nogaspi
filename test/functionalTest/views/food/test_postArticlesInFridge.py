from nogaspi.views.food.postArticlesInFridge import postArticlesInFridge
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import datetime
import pytest

def test_food_postArticlesInFridge():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = postArticlesInFridge(FakeRequest({
        "token": "token_toto",
        "articles": [
            {
                "barcode": "3267110001144",
                "expirationDate": str(datetime.date.today() + datetime.timedelta(days=14))
            },
            {
                "barcode": "3163937012007",
                "expirationDate": str(datetime.date.today() - datetime.timedelta(days=14))
            }
        ]
    }))
    assert funcRtr['isPosted']
    assert len(sqlSelect(table='article')) == 2
    assert sqlSelect(
        table='article',
        conditions="WHERE idProduct = (SELECT id FROM product WHERE barcode = '3267110001144')"
    )[0]['idFridge'] == 1
    assert sqlSelect(
        table='article',
        conditions="WHERE idProduct = (SELECT id FROM product WHERE barcode = '3163937012007')"
    )[0]['idFridge'] == 1

def test_food_postArticlesInFridge_with_bad_expiration_date():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        postArticlesInFridge(FakeRequest({
            "token": "token_toto",
            "articles": [
                {
                    "barcode": "3267110001144",
                    "expirationDate": str(datetime.date.today() + datetime.timedelta(days=14))
                },
                {
                    "barcode": "3163937012007",
                    "expirationDate": str(datetime.date.today() - datetime.timedelta(days=16)) #bad date
                }
            ]
        }))

def test_food_postArticlesInFridge_with_bad_barcode():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        postArticlesInFridge(FakeRequest({
            "token": "token_toto",
            "articles": [
            {
                "barcode": "0",
                "expirationDate": str(datetime.date.today() + datetime.timedelta(days=14))
            },
            {
                "barcode": "3163937012007",
                "expirationDate": str(datetime.date.today() - datetime.timedelta(days=14))
            }
        ]
        }))