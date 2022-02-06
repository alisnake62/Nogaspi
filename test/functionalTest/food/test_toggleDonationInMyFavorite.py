from nogaspi.views.food.toggleDonationInMyFavorite import toggleDonationInMyFavorite
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_food_toggleDonationInMyFavorite():
    querys = [
        "INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);",
        "INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `code`, `code_expiration`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, NOW(), '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = toggleDonationInMyFavorite(FakeRequest({"token":"token_tata", "idDonation": 1}))
    assert funcRtr['isFavorite']

    idDonationExpected = sqlSelect(table= 'favorite_donation', conditions='WHERE idUser = 2')[0]['idDonation']
    assert idDonationExpected == 1

    funcRtr = toggleDonationInMyFavorite(FakeRequest({"token":"token_tata", "idDonation": 1}))
    assert not funcRtr['isFavorite']
    favoriteDonationExpected = sqlSelect(table= 'favorite_donation', conditions='WHERE idUser = 2')
    assert len(favoriteDonationExpected) == 0

def test_food_toggleDonationInMyFavorite_with_my_donation():
    querys = [
        "INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `code`, `code_expiration`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, NOW(), '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        toggleDonationInMyFavorite(FakeRequest({"token":"token_toto", "idDonation": 1}))

def test_food_toggleDonationInMyFavorite_with_donation_does_not_exist():
    querys = [
        "INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);",
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        toggleDonationInMyFavorite(FakeRequest({"token":"token_toto", "idDonation": 1}))

def test_food_toggleDonationInMyFavorite_with_donation_is_archive():
    querys = [
        "INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);",
        "INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `code`, `code_expiration`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, NOW(), '1');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        toggleDonationInMyFavorite(FakeRequest({"token":"token_tata", "idDonation": 1}))

def test_food_toggleDonationInMyFavorite_with_donation_is_expired():
    querys = [
        "INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);",
        "INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `code`, `code_expiration`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, NOW(), '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        toggleDonationInMyFavorite(FakeRequest({"token":"token_tata", "idDonation": 1}))
    