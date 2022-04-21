from nogaspi.views.food.getProduct import Product
from nogaspi.views.register.login import User
from nogaspi.views.food.postArticlesInFridge import Article
from nogaspi.dbEngine import EngineSQLAlchemy
from datetime import datetime

def test_article_toJson():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        product = Product(toto, datetime.now(), "101010101")
        article = Article(product, donation=None, expirationDate=datetime(year=2122, month=1, day=1))
        session.add(toto)
        session.add(product)
        session.add(article)
        session.commit()

        assert article.toJson() == {
            'id': article.id,
            'product': product.toJson(),
            'expirationDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1)))
        }