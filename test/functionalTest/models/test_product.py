from nogaspi.views.food.getProduct import Product
from nogaspi.views.register.login import User
from nogaspi.views.food.getAllergens import Allergen
from test.functionalTest.dbMagement import sqlQuerysWithCommit
from nogaspi.dbEngine import EngineSQLAlchemy
from datetime import datetime

def test_product_toJson():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        product = Product(toto, datetime.now(), "101010101")
        product.opinion = "My Opinion"
        product.name = "My Name"
        product.brand = "My Brand"
        product.quantity = "My Quantity"
        product.image_url = "http://product.image"
        product.ingredients = "My Ingredient 1, My Ingredient 2"
        product.nutrimentData = "{\"Nutriment\":\"Nutriment1\"}"
        product.nutriscoreData = "{\"Nutriscore\":\"Nutriscore1\"}"
        allergen1 = Allergen("English1", "French1")
        allergen2 = Allergen("English2", "French2")
        session.add(toto)
        session.add(product)
        session.add(allergen1)
        session.add(allergen2)
        session.commit()
        querys = [
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('1', '{product.id}', '{allergen1.id}');",
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('2', '{product.id}', '{allergen2.id}');",
        ]
        for query in querys:
            session.execute(query)
        session.commit()

        assert product.toJson() == {
            'id': product.id,
            'opinion': "My Opinion",
            'name': "My Name",
            'brand': "My Brand",
            'quantity': "My Quantity",
            'barcode': "101010101",
            'image_url': "http://product.image",
            'ingredient' : "My Ingredient 1, My Ingredient 2",
            'nutrimentsData' : {"Nutriment": "Nutriment1"},
            'nutriscoreData' : {"Nutriscore": "Nutriscore1"},
            'allergens': ["French1", "French2"]
        }

def test_product_toJson_without_nutriscore_and_nutriments_datas():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        product = Product(toto, datetime.now(), "101010101")
        product.opinion = "My Opinion"
        product.name = "My Name"
        product.brand = "My Brand"
        product.quantity = "My Quantity"
        product.image_url = "http://product.image"
        product.ingredients = "My Ingredient 1, My Ingredient 2"
        allergen1 = Allergen("English1", "French1")
        allergen2 = Allergen("English2", "French2")
        session.add(toto)
        session.add(product)
        session.add(allergen1)
        session.add(allergen2)
        session.commit()
        querys = [
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('1', '{product.id}', '{allergen1.id}');",
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('2', '{product.id}', '{allergen2.id}');",
        ]
        for query in querys:
            session.execute(query)
        session.commit()

        assert product.toJson() == {
            'id': product.id,
            'opinion': "My Opinion",
            'name': "My Name",
            'brand': "My Brand",
            'quantity': "My Quantity",
            'barcode': "101010101",
            'image_url': "http://product.image",
            'ingredient' : "My Ingredient 1, My Ingredient 2",
            'nutrimentsData' : None,
            'nutriscoreData' : None,
            'allergens': ["French1", "French2"]
        }