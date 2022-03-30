from nogaspi.views.food.postDonationFromScan import postDonationFromScan
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest
import datetime

def test_food_postDonationFromScan():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); "
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = postDonationFromScan(FakeRequest({
        "token": "token_toto",
        "articles": [
            {"barcode": "3267110001144", "expirationDate":str(datetime.date.today() - datetime.timedelta(days=14))},
            {"barcode": "3163937012007", "expirationDate":str(datetime.date.today() + datetime.timedelta(days=5))}
        ],
        "latitude": 43.5,
        "longitude": 1.5,
        "geoPrecision": 500,
        "endingDate": str(datetime.date.today() + datetime.timedelta(days=14))
    }))
    assert funcRtr['isPosted']
    assert len(sqlSelect(table='donation')) == 1
    assert len(sqlSelect(table='product')) == 2
    assert len(sqlSelect(table='article')) == 2
    assert sqlSelect(
        table='article',
        conditions="WHERE idProduct = (SELECT id FROM product WHERE barcode = '3267110001144')"
    )[0]['idDonation'] == sqlSelect(table='donation')[0]['id']
    assert sqlSelect(
        table='article',
        conditions="WHERE idProduct = (SELECT id FROM product WHERE barcode = '3163937012007')"
    )[0]['idDonation'] == sqlSelect(table='donation')[0]['id']
    assert sqlSelect(table='donation')[0]["latitude"] == 43.5
    assert sqlSelect(table='donation')[0]["longitude"] == 1.5
    assert sqlSelect(table='donation')[0]["geoPrecision"] == 500

def test_food_postDonationFromScan_with_barcode_already_present_in_db():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); ",
        "INSERT INTO `product` (`id`, `barcode`, `idLastScanUser`, `lastScanDate`) VALUES (1, '3267110001144', '1', NOW())"    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = postDonationFromScan(FakeRequest({
        "token": "token_toto",
        "articles": [
            {"barcode": "3267110001144", "expirationDate":str(datetime.date.today() - datetime.timedelta(days=14))},
            {"barcode": "3163937012007", "expirationDate":str(datetime.date.today() + datetime.timedelta(days=5))}
        ],
        "latitude": 43.5,
        "longitude": 1.5,
        "geoPrecision": 500,
        "endingDate": str(datetime.date.today() + datetime.timedelta(days=14))
    }))
    assert funcRtr['isPosted']
    assert len(sqlSelect(table='donation')) == 1
    assert len(sqlSelect(table='product')) == 2
    assert len(sqlSelect(table='article')) == 2
    assert sqlSelect(
        table='article',
        conditions="WHERE idProduct = (SELECT id FROM product WHERE barcode = '3267110001144')"
    )[0]['idDonation'] == sqlSelect(table='donation')[0]['id']
    assert sqlSelect(
        table='article',
        conditions="WHERE idProduct = (SELECT id FROM product WHERE barcode = '3163937012007')"
    )[0]['idDonation'] == sqlSelect(table='donation')[0]['id']
    assert sqlSelect(table='donation')[0]["latitude"] == 43.5
    assert sqlSelect(table='donation')[0]["longitude"] == 1.5
    assert sqlSelect(table='donation')[0]["geoPrecision"] == 500

def test_food_postDonationFromScan_without_fridge():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');"
    ]
    sqlQuerysWithCommit(querys)

    funcRtr = postDonationFromScan(FakeRequest({
        "token": "token_toto",
        "articles": [
            {"barcode": "3267110001144", "expirationDate":str(datetime.date.today() + datetime.timedelta(days=5))},
            {"barcode": "3163937012007", "expirationDate":str(datetime.date.today() + datetime.timedelta(days=5))}
        ],
        "latitude": 43.5,
        "longitude": 1.5,
        "geoPrecision": 500,
        "endingDate": str(datetime.date.today() + datetime.timedelta(days=14))
    }))

    assert funcRtr['isPosted']
    assert len(sqlSelect(table='donation')) == 1
    assert len(sqlSelect(table='product')) == 2
    assert len(sqlSelect(table='article')) == 2
    assert len(sqlSelect(table='fridge')) == 1
    assert sqlSelect(
        table='article',
        conditions="WHERE idProduct = (SELECT id FROM product WHERE barcode = '3267110001144')"
    )[0]['idDonation'] == sqlSelect(table='donation')[0]['id']
    assert sqlSelect(
        table='article',
        conditions="WHERE idProduct = (SELECT id FROM product WHERE barcode = '3163937012007')"
    )[0]['idDonation'] == sqlSelect(table='donation')[0]['id']
    assert sqlSelect(table='article')[0]['idFridge'] == sqlSelect(table='fridge')[0]['id']
    assert sqlSelect(table='donation')[0]["latitude"] == 43.5
    assert sqlSelect(table='donation')[0]["longitude"] == 1.5
    assert sqlSelect(table='donation')[0]["geoPrecision"] == 500

def test_food_postDonationFromScan_with_bad_barcode():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1');"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        postDonationFromScan(FakeRequest({
            "token": "token_toto",
            "articles": [
                {"barcode": "10101010", "expirationDate":str(datetime.date.today() + datetime.timedelta(days=5))},
                {"barcode": "3163937012007", "expirationDate":str(datetime.date.today() + datetime.timedelta(days=5))}
            ],
            "latitude": 43.5,
            "longitude": 1.5,
            "geoPrecision": 500,
            "endingDate": str(datetime.date.today() + datetime.timedelta(days=14))
        }))

def test_food_postDonationFromScan_with_bad_expiration_date():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1');"
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        postDonationFromScan(FakeRequest({
            "token": "token_toto",
            "articles": [
                {"barcode": "3267110001144", "expirationDate": str(datetime.date.today() - datetime.timedelta(days=16))},
                {"barcode": "3163937012007", "expirationDate": str(datetime.date.today() + datetime.timedelta(days=5))}
            ],
            "latitude": 43.5,
            "longitude": 1.5,
            "geoPrecision": 500,
            "endingDate": str(datetime.date.today() + datetime.timedelta(days=14))
        }))

def test_food_postDonationFromScan_with_bad_ending_date():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `fridge` (`id`, `idUser`) VALUES ('1', '1'); "
    ]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        postDonationFromScan(FakeRequest({
            "token": "token_toto",
            "articles": [
                {"barcode": "3267110001144", "expirationDate":str(datetime.date.today() - datetime.timedelta(days=14))},
                {"barcode": "3163937012007", "expirationDate":str(datetime.date.today() + datetime.timedelta(days=5))}
            ],
            "latitude": 43.5,
            "longitude": 1.5,
            "geoPrecision": 500,
            "endingDate": str(datetime.date.today() - datetime.timedelta(days=1))
        }))