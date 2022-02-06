from nogaspi.views.food.toggleDonationInMyFavorite import toggleDonationInMyFavorite
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlQuery
from test.functionalTest.flaskManagement import FakeRequest

def test_food_toggleDonationInMyFavorite():
    querys = []
    querys.append("INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);")
    querys.append("INSERT INTO `user` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `idRang`, `points`, `regularPathLatitudeStart`, `regularPathLongitudeStart`, `regularPathLatitudeEnd`, `regularPathLongitudeEnd`, `regularPathPoints`, `fireBaseToken`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, NULL, '0', NULL, NULL, NULL, NULL, NULL, NULL);")
    querys.append("INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `code`, `code_expiration`, `archive`) VALUES ('1', '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, NOW(), '0');")
    sqlQuerysWithCommit(querys)
    
    funcRtr = toggleDonationInMyFavorite(FakeRequest({"token":"token_tata", "idDonation": 1}))
    assert funcRtr['isFavorite']
    idDonationExpected = sqlQuery("SELECT * from favorite_donation WHERE favorite_donation.idUser = 2")[0][2]
    assert idDonationExpected == 1

    funcRtr = toggleDonationInMyFavorite(FakeRequest({"token":"token_tata", "idDonation": 1}))
    assert not funcRtr['isFavorite']
    favoriteDonationExpected = sqlQuery("SELECT * from favorite_donation WHERE favorite_donation.idUser = 2")
    assert len(favoriteDonationExpected) == 0