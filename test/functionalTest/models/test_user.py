from nogaspi.views.register.login import User
from nogaspi.dbEngine import EngineSQLAlchemy
import os

def test_user_toJson():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        toto.rating = 2.4
        toto.ratingCount = 4
        session.add(toto)
        session.commit()

        assert toto.toJson() == {
            'id': toto.id,
            'mail': "toto@toto.fr",
            'pseudo': "toto",
            'points': 0,
            'profilePictureUrl': f"http://{os.environ['SERVER_ADRESS']}:49080/users/image_toto.jpg",
            'rating':{
                'average': 2.4,
                'count': 4
            }
        }