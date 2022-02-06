def makeDonation(userOwner, userTaker, donation):
    donation.archive = True
    articleCount = len(donation.articles)
    for article in donation.articles:
        article.fridge = None
    userTaker.points += articleCount
    userOwner.points += articleCount * 4