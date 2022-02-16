"""

from nogaspi.views.food.getAllergens import getAllergens
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest

def test_object_Allergen():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `allergen` (`id`, `nameEN`, `nameFR`) VALUES (1, 'peanuts', 'cacahuete');",
        "INSERT INTO `allergen` (`id`, `nameEN`, `nameFR`) VALUES (2, 'milk', 'lait');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getAllergens(FakeRequest({"token":"token_toto"}))
    assert funcRtr['allergens'] == ['cacahuete', 'lait']"""