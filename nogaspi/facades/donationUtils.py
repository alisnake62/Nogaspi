def makeDonation(userOwner, userTaker, donation):
    donation.archive = True
    for article in donation.articles:
        article.fridge = None
    userTaker.points += 5
    userOwner.points += 20