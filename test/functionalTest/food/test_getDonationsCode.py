from nogaspi.views.food.getDonationsCode import getDonationsCode
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest
import datetime

def test_food_getDonationsCode():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getDonationsCode(FakeRequest({"token":"token_toto", "idDonations": "1,2"}))
    assert len(funcRtr["code"]) == 64
    assert sqlSelect(table='donationCode', conditions='WHERE id = 1')[0]['code'] == funcRtr["code"]
    assert sqlSelect(table='donation', conditions='WHERE id = 1')[0]['idDonationCode'] == 1
    assert sqlSelect(table='donation', conditions='WHERE id = 2')[0]['idDonationCode'] == 1
    assert sqlSelect(table='donationCode', conditions='WHERE id = 1')[0]['expirationDate'] > datetime.datetime.now()
    assert sqlSelect(table='donationCode', conditions='WHERE id = 1')[0]['expirationDate'] < datetime.datetime.now() + datetime.timedelta(minutes = 10)
