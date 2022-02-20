
from nogaspi.views.food.generateDonationsCode import DonationCode
from nogaspi.dbEngine import EngineSQLAlchemy
from datetime import datetime

def test_donationCode_toJson():
    with EngineSQLAlchemy() as session:
        donationCode = DonationCode()
        donationCode.code = "101010101"
        donationCode.expirationDate = datetime(year=2122, month=1, day=1)
        session.add(donationCode)
        session.commit()

        assert donationCode.toJson() == {
            'code': "101010101",
            'expirationDate': int(datetime.timestamp(datetime(year=2122, month=1, day=1)))
        }