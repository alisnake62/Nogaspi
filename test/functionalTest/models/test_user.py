from nogaspi.views.register.login import User
from nogaspi.views.food.getAllergens import Allergen
from nogaspi.dbEngine import EngineSQLAlchemy
import os

def test_user_toJson():
    with EngineSQLAlchemy() as session:
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        allergen = Allergen('peanuts')
        toto.rating = 2.4
        toto.ratingCount = 4
        toto.address = "1 avenue du chapeau 66666 Chaussette"
        toto.allergen = allergen
        toto.favoriteDistanceToSearch = 500
        toto.favoriteGeoPrecisionToDonate = 600
        session.add(toto)
        session.commit()

        assert toto.toJson(userRequester=titi) == {
            'id': toto.id,
            'mail': "toto@toto.fr",
            'pseudo': "toto",
            'points': 0,
            'profilePictureUrl': f"http://{os.environ['SERVER_ADDRESS']}:49080/users/image_toto.jpg",
            'rating':{
                'average': 2.4,
                'count': 4
            }
        }

        assert toto.toJson()['profilePictureUrl'] in ("http://localhost:49080/users/image_toto.jpg", "http://monappli.ovh:49080/users/image_toto.jpg")

def test_user_toJson_if_its_me():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        toto.rating = 2.4
        toto.ratingCount = 4
        session.add(toto)
        session.commit()

        assert toto.toJson(userRequester=toto) == {
            'id': toto.id,
            'mail': "toto@toto.fr",
            'pseudo': "toto",
            'points': 0,
            'profilePictureUrl': f"http://{os.environ['SERVER_ADDRESS']}:49080/users/image_toto.jpg",
            'rating':{
                'average': 2.4,
                'count': 4
            },
            'address': None,
            'allergen': None,
            'favoriteDistanceToSearch': None,
            'favoriteGeoPrecisionToDonate': None
        }

        assert toto.toJson()['profilePictureUrl'] in ("http://localhost:49080/users/image_toto.jpg", "http://monappli.ovh:49080/users/image_toto.jpg")


def test_user_toJson_if_its_me2():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        allergen = Allergen('peanuts')
        toto.rating = 2.4
        toto.ratingCount = 4
        toto.address = "1 avenue du chapeau 66666 Chaussette"
        toto.allergen = allergen
        toto.favoriteDistanceToSearch = 500
        toto.favoriteGeoPrecisionToDonate = 600
        session.add(toto)
        session.commit()

        assert toto.toJson(userRequester=toto) == {
            'id': toto.id,
            'mail': "toto@toto.fr",
            'pseudo': "toto",
            'points': 0,
            'profilePictureUrl': f"http://{os.environ['SERVER_ADDRESS']}:49080/users/image_toto.jpg",
            'rating':{
                'average': 2.4,
                'count': 4
            },
            'address': "1 avenue du chapeau 66666 Chaussette",
            'allergen': 'peanuts',
            'favoriteDistanceToSearch': 500,
            'favoriteGeoPrecisionToDonate': 600
        }

        assert toto.toJson()['profilePictureUrl'] in ("http://localhost:49080/users/image_toto.jpg", "http://monappli.ovh:49080/users/image_toto.jpg")