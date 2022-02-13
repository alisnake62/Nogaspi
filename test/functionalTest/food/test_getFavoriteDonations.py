from nogaspi.views.food.getFavoriteDonations import getFavoriteDonations
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest

def test_food_getFavoriteDonations():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('3', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `favorite_donation` (`id`, `idUser`, `idDonation`) VALUES (NULL, '1', '1')",
        "INSERT INTO `favorite_donation` (`id`, `idUser`, `idDonation`) VALUES (NULL, '1', '3')"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getFavoriteDonations(FakeRequest({"token":"token_toto"}))
    assert [d['id'] for d in funcRtr['favoriteDonations']] == [1, 3]

def test_food_getFavoriteDonations_with_bad_user():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('1', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('2', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES ('3', '1', '43.6', '1.5', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `favorite_donation` (`id`, `idUser`, `idDonation`) VALUES (NULL, '1', '1')",
        "INSERT INTO `favorite_donation` (`id`, `idUser`, `idDonation`) VALUES (NULL, '1', '3')"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getFavoriteDonations(FakeRequest({"token":"token_tata"}))
    assert [d['id'] for d in funcRtr['favoriteDonations']] == []