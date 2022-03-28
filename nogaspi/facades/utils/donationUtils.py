def makeDonation(userOwner, userTaker, donation):
    donation.archive = True
    donation.userTaker = userTaker
    articleCount = len(donation.articles)
    for article in donation.articles:
        article.fridge = None
    userTaker.points += articleCount
    userOwner.points += articleCount * 4
    return articleCount * 4

def updateRatingUser(user, note):
    ratingCount = user.ratingCount
    rating = user.rating
    newRating = (rating * ratingCount + note) / (ratingCount + 1)
    user.rating = newRating
    user.ratingCount = ratingCount + 1