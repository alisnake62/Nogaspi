from nogaspi.views.register.checkTokenValidity import checkTokenValidityTest
from test.functionalTest.dbMagement import sqlQuery
import datetime

def test_register_checkTokenValidity():
    timeAfterNow = datetime.datetime.now() + datetime.timedelta(minutes = 15)
    sqlQuery([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    fnrtr = checkTokenValidityTest("token_toto")
    
    sqlQuery([f"DELETE FROM `user` WHERE `user`.`id` = 1"])
    
    assert fnrtr['validity']
    assert fnrtr['user'] == 'toto@toto.fr'


def test_register_checkTokenValidity_with_bad_Token():
    timeAfterNow = datetime.datetime.now() + datetime.timedelta(minutes = 15)
    sqlQuery([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    fnrtr = checkTokenValidityTest("token_tata")
    
    sqlQuery([f"DELETE FROM `user` WHERE `user`.`id` = 1"])

    assert fnrtr == {'validity': False, 'user' : 'Unknown', 'token_expiration': 'Unknown'}

def test_register_checkTokenValidity_with_bad_expirationDate():
    timeAfterNow = datetime.datetime.now() - datetime.timedelta(minutes = 15)
    sqlQuery([f"INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', '{timeAfterNow}', NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);"])
    
    fnrtr = checkTokenValidityTest("token_toto")
    
    sqlQuery([f"DELETE FROM `user` WHERE `user`.`id` = 1"])

    assert not fnrtr['validity']
    assert fnrtr['user'] == 'toto@toto.fr'
