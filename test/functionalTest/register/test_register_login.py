from nogaspi.facades.apiConfig.apiResponse import APIException
from nogaspi.views.register.login import login
from test.functionalTest.dbMagement import sqlQuery, sqlDeleteAllData
from test.functionalTest.flaskManagement import FakeRequest
import datetime
import pytest

def test_register_login():
    timeAfterNow = datetime.datetime.now()
    sqlQuery([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    inputRequest = {
    "mail":"toto@toto.fr",
    "password":"toto"
    }
    fnrtr = login(inputRequest, FakeRequest())
    
    sqlDeleteAllData()
    
    assert len(fnrtr['token']) == 64
    assert 'token_expiration' in fnrtr

def test_register_login_with_bad_password():
    timeAfterNow = datetime.datetime.now()
    sqlQuery([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    inputRequest = {
    "mail":"toto@toto.fr",
    "password":"tata"
    }
    with pytest.raises(Exception):
        login(inputRequest, FakeRequest())
    
    sqlDeleteAllData()

def test_register_login_with_bad_user():
    timeAfterNow = datetime.datetime.now()
    sqlQuery([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, NULL, '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    inputRequest = {
    "mail":"toto@tata.fr",
    "password":"toto"
    }
    with pytest.raises(Exception):
        login(inputRequest, FakeRequest())
    
    sqlDeleteAllData()
    