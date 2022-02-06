from models.objectDB import Article, Fridge
from dbEngine import EngineSQLAlchemy
from facades.apiConfig import EmptyException, DonationException, FridgeException, getArgs
from facades.utils.registerUtils import getUserFromToken


def deleteArticlesInFridge(request):

    token, idArticles = getArgs(request, ['token', 'idArticles'])

    with EngineSQLAlchemy() as session:

        user = getUserFromToken(token, session, request)
        user.majTokenValidity()

        fridge = session.query( Fridge ).filter(Fridge.user == user).first()
        if not fridge:
            message = "You don't have fridge, please post minimum one article to create your fridge"
            raise EmptyException(message, message, request)

        for idArticle in idArticles:
            
            article = session.query( Article ).filter(Article.id == idArticle).first()
            if not article: 
                message = "The article {} is unknow".format(idArticle)
                raise EmptyException(message, message, request)

            if article.fridge != fridge:
                message = "The article {} is not in you fridge".format(idArticle)
                raise FridgeException(message, message, request)

            if article.donation is not None:
                if article.donation.isValide():
                    message = "The article {} is in a valid Donation {}, please delete the donation to be able to remote this article from fridge".format(article.id, article.donation.id)
                    raise DonationException(message, message, request)

        for idArticle in idArticles:

            article = session.query( Article ).filter(Article.id == idArticle).first()
            article.fridge = None

        session.commit()

        data = {'isDelete (Remove from fridge)':True}

    return data