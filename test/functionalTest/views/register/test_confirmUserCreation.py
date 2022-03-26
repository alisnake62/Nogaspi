import datetime
from nogaspi.views.register.confirmUserCreation import confirmUserCreation
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_register_confirmUserCreation():

    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`, `confirmationCode`, `confirmationCodeExpiration`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', '0', '1234567890', NOW() + INTERVAL 1 DAY);"]
    sqlQuerysWithCommit(querys)

    funcRtr = confirmUserCreation(FakeRequest({
        "mail":"toto@toto.fr",
        "confirmationCode": "1234567890"
    }))
    
    assert funcRtr['isConfirmate']
    assert sqlSelect(table="userNogaspi", conditions="WHERE id = 1")[0]['isConfirmate'] == 1


def test_register_confirmUserCreation_with_expirate_confirmate_code():

    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`, `confirmationCode`, `confirmationCodeExpiration`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', '0', '1234567890', NOW() - INTERVAL 1 MINUTE);"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        confirmUserCreation(FakeRequest({
            "mail":"toto@toto.fr",
            "confirmationCode": "1234567890"
        }))

def test_register_confirmUserCreation_with_bad_confirmation_code():

    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`, `confirmationCode`, `confirmationCodeExpiration`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', '0', '1234567890', NOW() + INTERVAL 1 DAY);"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        confirmUserCreation(FakeRequest({
            "mail":"toto@toto.fr",
            "confirmationCode": "ABCDEFGHIJ"
        }))

def test_register_confirmUserCreation_with_bad_user():

    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`, `confirmationCode`, `confirmationCodeExpiration`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', '0', '1234567890', NOW() + INTERVAL 1 DAY);"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        confirmUserCreation(FakeRequest({
            "mail":"titi@titi.fr",
            "confirmationCode": "1234567890"
        }))

def test_register_confirmUserCreation_if_user_already_confirmate():

    querys = ["INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `isConfirmate`, `confirmationCode`, `confirmationCodeExpiration`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', '1', '1234567890', NOW() + INTERVAL 1 DAY);"]
    sqlQuerysWithCommit(querys)

    with pytest.raises(Exception):
        confirmUserCreation(FakeRequest({
            "mail":"toto@toto.fr",
            "confirmationCode": "1234567890"
        }))