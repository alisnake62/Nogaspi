from nogaspi.views.register.login import User
from nogaspi.views.food.getByBarCode import Product
from nogaspi.views.food.postArticlesInFridge import Article
from nogaspi.views.food.getDonations import Donation
from nogaspi.views.food.getAllergens import Allergen
from nogaspi.views.messaging.initiateConversation import Message, Conversation
from nogaspi.dbEngine import EngineSQLAlchemy
from datetime import datetime

def test_donation_toJson():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        tata = User("tata@tata.fr", "tata_password", "tata", "image_tata.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        donation.startingDate = datetime(year=2022, month=1, day=1)
        conversation1 = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message1 = Message(conversation=conversation1, toDonator=True, body="My Message")
        conversation2 = Conversation(donation=donation, userDonator=toto, userTaker=tata)
        message2 = Message(conversation=conversation2, toDonator=True, body="My Message")
        product = Product(toto, datetime.now(), "101010101")
        article1 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        article2 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        allergen1 = Allergen("English1", "French1")
        allergen2 = Allergen("English2", "French2")
        session.add(toto)
        session.add(titi)
        session.add(tata)
        session.add(donation)
        session.add(conversation1)
        session.add(message1)
        session.add(conversation2)
        session.add(message2)
        session.add(product)
        session.add(article1)
        session.add(article2)
        session.add(allergen1)
        session.add(allergen2)
        session.commit()
        querys = [
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('1', '{product.id}', '{allergen1.id}');",
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('2', '{product.id}', '{allergen2.id}');",
            f"INSERT INTO `favorite_donation` (`id`, `idUser`, `idDonation`) VALUES ('1', '{titi.id}', '{donation.id}');",
        ]
        for query in querys:
            session.execute(query)
        session.commit()

        assert donation.toJson(userRequester=titi) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': False,
            'isValide': True,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': False,
            'myTakerConversationInfo': conversation1.toJsonlight(titi),
            'myDonatorConversationsInfo': None,
            'isMyFavorite': True,
            'userTaker': None,
            'rating': None
        }
        assert donation.toJson(userRequester=toto) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': False,
            'isValide': True,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': True,
            'myTakerConversationInfo': None,
            'myDonatorConversationsInfo': [conversation1.toJsonlight(toto), conversation2.toJsonlight(toto)],
            'isMyFavorite': False,
            'userTaker': None,
            'rating': None
        }

def test_donation_toJson_without_conversation():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        tata = User("tata@tata.fr", "tata_password", "tata", "image_tata.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        donation.startingDate = datetime(year=2022, month=1, day=1)
        product = Product(toto, datetime.now(), "101010101")
        article1 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        article2 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        allergen1 = Allergen("English1", "French1")
        allergen2 = Allergen("English2", "French2")
        session.add(toto)
        session.add(titi)
        session.add(tata)
        session.add(donation)
        session.add(product)
        session.add(article1)
        session.add(article2)
        session.add(allergen1)
        session.add(allergen2)
        session.commit()
        querys = [
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('1', '{product.id}', '{allergen1.id}');",
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('2', '{product.id}', '{allergen2.id}');",
            f"INSERT INTO `favorite_donation` (`id`, `idUser`, `idDonation`) VALUES ('1', '{titi.id}', '{donation.id}');",
        ]
        for query in querys:
            session.execute(query)
        session.commit()

        assert donation.toJson(userRequester=titi) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': False,
            'isValide': True,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': False,
            'myTakerConversationInfo': None,
            'myDonatorConversationsInfo': None,
            'isMyFavorite': True,
            'userTaker': None,
            'rating': None
        }
        assert donation.toJson(userRequester=toto) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': False,
            'isValide': True,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': True,
            'myTakerConversationInfo': None,
            'myDonatorConversationsInfo': [],
            'isMyFavorite': False,
            'userTaker': None,
            'rating': None
        }

def test_donation_toJson_with_expired_donation():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        tata = User("tata@tata.fr", "tata_password", "tata", "image_tata.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2022, month=1, day=2))
        donation.startingDate = datetime(year=2022, month=1, day=1)
        conversation1 = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message1 = Message(conversation=conversation1, toDonator=True, body="My Message")
        conversation2 = Conversation(donation=donation, userDonator=toto, userTaker=tata)
        message2 = Message(conversation=conversation2, toDonator=True, body="My Message")
        product = Product(toto, datetime.now(), "101010101")
        article1 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        article2 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        allergen1 = Allergen("English1", "French1")
        allergen2 = Allergen("English2", "French2")
        session.add(toto)
        session.add(titi)
        session.add(tata)
        session.add(donation)
        session.add(conversation1)
        session.add(message1)
        session.add(conversation2)
        session.add(message2)
        session.add(product)
        session.add(article1)
        session.add(article2)
        session.add(allergen1)
        session.add(allergen2)
        session.commit()
        querys = [
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('1', '{product.id}', '{allergen1.id}');",
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('2', '{product.id}', '{allergen2.id}');",
            f"INSERT INTO `favorite_donation` (`id`, `idUser`, `idDonation`) VALUES ('1', '{titi.id}', '{donation.id}');",
        ]
        for query in querys:
            session.execute(query)
        session.commit()

        assert donation.toJson(userRequester=titi) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=2))),
            'isExpired': True,
            'isArchived': False,
            'isValide': False,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': False,
            'myTakerConversationInfo': conversation1.toJsonlight(titi),
            'myDonatorConversationsInfo': None,
            'isMyFavorite': True,
            'userTaker': None,
            'rating': None
        }
        assert donation.toJson(userRequester=toto) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=2))),
            'isExpired': True,
            'isArchived': False,
            'isValide': False,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': True,
            'myTakerConversationInfo': None,
            'myDonatorConversationsInfo': [conversation1.toJsonlight(toto), conversation2.toJsonlight(toto)],
            'isMyFavorite': False,
            'userTaker': None,
            'rating': None
        }

def test_donation_toJson_with_archived_donation():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        tata = User("tata@tata.fr", "tata_password", "tata", "image_tata.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        donation.startingDate = datetime(year=2022, month=1, day=1)
        donation.archive = 1
        conversation1 = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message1 = Message(conversation=conversation1, toDonator=True, body="My Message")
        conversation2 = Conversation(donation=donation, userDonator=toto, userTaker=tata)
        message2 = Message(conversation=conversation2, toDonator=True, body="My Message")
        product = Product(toto, datetime.now(), "101010101")
        article1 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        article2 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        allergen1 = Allergen("English1", "French1")
        allergen2 = Allergen("English2", "French2")
        session.add(toto)
        session.add(titi)
        session.add(tata)
        session.add(donation)
        session.add(conversation1)
        session.add(message1)
        session.add(conversation2)
        session.add(message2)
        session.add(product)
        session.add(article1)
        session.add(article2)
        session.add(allergen1)
        session.add(allergen2)
        session.commit()
        querys = [
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('1', '{product.id}', '{allergen1.id}');",
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('2', '{product.id}', '{allergen2.id}');",
            f"INSERT INTO `favorite_donation` (`id`, `idUser`, `idDonation`) VALUES ('1', '{titi.id}', '{donation.id}');",
        ]
        for query in querys:
            session.execute(query)
        session.commit()

        assert donation.toJson(userRequester=titi) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': True,
            'isValide': False,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': False,
            'myTakerConversationInfo': conversation1.toJsonlight(titi),
            'myDonatorConversationsInfo': None,
            'isMyFavorite': True,
            'userTaker': None,
            'rating': None
        }
        assert donation.toJson(userRequester=toto) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': True,
            'isValide': False,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': True,
            'myTakerConversationInfo': None,
            'myDonatorConversationsInfo': [conversation1.toJsonlight(toto), conversation2.toJsonlight(toto)],
            'isMyFavorite': False,
            'userTaker': None,
            'rating': None
        }

def test_donation_toJson_with_archived_and_rating_donation():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        tata = User("tata@tata.fr", "tata_password", "tata", "image_tata.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        donation.startingDate = datetime(year=2022, month=1, day=1)
        donation.archive = 1
        donation.rating = 4
        donation.userTaker = titi
        conversation1 = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message1 = Message(conversation=conversation1, toDonator=True, body="My Message")
        conversation2 = Conversation(donation=donation, userDonator=toto, userTaker=tata)
        message2 = Message(conversation=conversation2, toDonator=True, body="My Message")
        product = Product(toto, datetime.now(), "101010101")
        article1 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        article2 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        allergen1 = Allergen("English1", "French1")
        allergen2 = Allergen("English2", "French2")
        session.add(toto)
        session.add(titi)
        session.add(tata)
        session.add(donation)
        session.add(conversation1)
        session.add(message1)
        session.add(conversation2)
        session.add(message2)
        session.add(product)
        session.add(article1)
        session.add(article2)
        session.add(allergen1)
        session.add(allergen2)
        session.commit()
        querys = [
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('1', '{product.id}', '{allergen1.id}');",
            f"INSERT INTO `product_allergen` (`id`, `idProduct`, `idAllergen`) VALUES ('2', '{product.id}', '{allergen2.id}');",
            f"INSERT INTO `favorite_donation` (`id`, `idUser`, `idDonation`) VALUES ('1', '{titi.id}', '{donation.id}');",
        ]
        for query in querys:
            session.execute(query)
        session.commit()

        assert donation.toJson(userRequester=titi) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': True,
            'isValide': False,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': False,
            'myTakerConversationInfo': conversation1.toJsonlight(titi),
            'myDonatorConversationsInfo': None,
            'isMyFavorite': True,
            'userTaker': titi.toJson(),
            'rating': 4
        }
        assert donation.toJson(userRequester=toto) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': True,
            'isValide': False,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': True,
            'myTakerConversationInfo': None,
            'myDonatorConversationsInfo': [conversation1.toJsonlight(toto), conversation2.toJsonlight(toto)],
            'isMyFavorite': False,
            'userTaker': titi.toJson(),
            'rating': 4
        }

def test_donation_toJson_with_not_favorite():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        tata = User("tata@tata.fr", "tata_password", "tata", "image_tata.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        donation.startingDate = datetime(year=2022, month=1, day=1)
        conversation1 = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message1 = Message(conversation=conversation1, toDonator=True, body="My Message")
        conversation2 = Conversation(donation=donation, userDonator=toto, userTaker=tata)
        message2 = Message(conversation=conversation2, toDonator=True, body="My Message")
        product = Product(toto, datetime.now(), "101010101")
        article1 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        article2 = Article(product, donation=donation, expirationDate=datetime(year=2122, month=1, day=1))
        allergen1 = Allergen("English1", "French1")
        allergen2 = Allergen("English2", "French2")
        session.add(toto)
        session.add(titi)
        session.add(tata)
        session.add(donation)
        session.add(conversation1)
        session.add(message1)
        session.add(conversation2)
        session.add(message2)
        session.add(product)
        session.add(article1)
        session.add(article2)
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

        assert donation.toJson(userRequester=titi) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': False,
            'isValide': True,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': False,
            'myTakerConversationInfo': conversation1.toJsonlight(titi),
            'myDonatorConversationsInfo': None,
            'isMyFavorite': False,
            'userTaker': None,
            'rating': None
        }
        assert donation.toJson(userRequester=toto) == {
            'id': donation.id,
            'latitude': 45,
            'longitude': 3,
            'geoPrecision': 500,
            'startingDate': int(datetime.timestamp(datetime(year=2022, month=1, day=1))),
            'endingDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'isExpired': False,
            'isArchived': False,
            'isValide': True,
            'articles': [article1.toJson(), article2.toJson()],
            'allergens': ["French1", "French2"],
            'owner': toto.toJson(),
            'isMine': True,
            'myTakerConversationInfo': None,
            'myDonatorConversationsInfo': [conversation1.toJsonlight(toto), conversation2.toJsonlight(toto)],
            'isMyFavorite': False,
            'userTaker': None,
            'rating': None
        }