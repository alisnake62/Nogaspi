from nogaspi.views.register.login import User
from nogaspi.views.food.getProduct import Product
from nogaspi.views.food.postArticlesInFridge import Article
from nogaspi.views.food.getDonations import Donation
from nogaspi.views.food.postArticlesInFridge import Fridge
from nogaspi.views.food.getAllergens import Allergen
from nogaspi.views.messaging.initiateConversation import Message, Conversation
from nogaspi.dbEngine import EngineSQLAlchemy
from datetime import datetime, timedelta

def test_fridge_toJson():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        fridge = Fridge(toto)
        product = Product(toto, datetime.now(), "101010101")
        article1 = Article(product, donation=None, expirationDate=datetime(year=2122, month=1, day=1), fridge=fridge)
        article2 = Article(product, donation=None, expirationDate=datetime(year=2122, month=1, day=1), fridge=fridge)
        session.add(toto)
        session.add(fridge)
        session.add(product)
        session.add(article1)
        session.add(article2)
        session.commit()

        assert fridge.toJson() == {            
            'articles': [article1.toJson(), article2.toJson()]
        }

def test_fridge_toJson_without_articles():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        fridge = Fridge(toto)
        session.add(toto)
        session.add(fridge)
        session.commit()

        assert fridge.toJson() == {            
            'articles': []
        }

def test_fridge_toJson_with_expired_article_more_than_tolerance_delta():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        fridge = Fridge(toto)
        product = Product(toto, datetime.now(), "101010101")
        article1 = Article(product, donation=None, expirationDate=datetime(year=2122, month=1, day=1), fridge=fridge)
        article2 = Article(product, donation=None, expirationDate=datetime.now() - timedelta(days=16), fridge=fridge)
        session.add(toto)
        session.add(fridge)
        session.add(product)
        session.add(article1)
        session.add(article2)
        session.commit()

        assert fridge.toJson() == {            
            'articles': [article1.toJson()]
        }

def test_fridge_toJson_with_expired_article_less_than_tolerance_delta():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        fridge = Fridge(toto)
        product = Product(toto, datetime.now(), "101010101")
        article1 = Article(product, donation=None, expirationDate=datetime(year=2122, month=1, day=1), fridge=fridge)
        article2 = Article(product, donation=None, expirationDate=datetime.now() - timedelta(days=14), fridge=fridge)
        session.add(toto)
        session.add(fridge)
        session.add(product)
        session.add(article1)
        session.add(article2)
        session.commit()

        assert fridge.toJson() == {            
            'articles': [article1.toJson(), article2.toJson()]
        }