from nogaspi.views.register.login import User
from nogaspi.views.messaging.initiateConversation import Message, Conversation
from nogaspi.views.food.getDonations import Donation
from nogaspi.dbEngine import EngineSQLAlchemy
from datetime import datetime

def test_message_toJson():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "http://toto.image")
        titi = User("titi@titi.fr", "titi_password", "titi", "http://titi.image")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        conversation = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message = Message(conversation=conversation, toDonator=True, body="My Message")
        message.dateTime = datetime(year=2122, month=1, day=1)
        session.add(toto)
        session.add(titi)
        session.add(donation)
        session.add(conversation)
        session.add(message)
        session.commit()

        assert message.toJson(userRequester=titi) == {
            'id': message.id,
            'readed': False,
            'dateTime': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'body': "My Message",
            'userFrom': titi.toJson(),
            'userTo': toto.toJson(),
            'isAMessageFromMe': True
        }
        assert message.toJson(userRequester=toto) == {
            'id': message.id,
            'readed': False,
            'dateTime': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'body': "My Message",
            'userFrom': titi.toJson(),
            'userTo': toto.toJson(),
            'isAMessageFromMe': False
        }

def test_message_toJson_to_taker():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "http://toto.image")
        titi = User("titi@titi.fr", "titi_password", "titi", "http://titi.image")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        conversation = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message = Message(conversation=conversation, toDonator=False, body="My Message")
        message.dateTime = datetime(year=2122, month=1, day=1)
        session.add(toto)
        session.add(titi)
        session.add(donation)
        session.add(conversation)
        session.add(message)
        session.commit()

        assert message.toJson(userRequester=titi) == {
            'id': message.id,
            'readed': False,
            'dateTime': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'body': "My Message",
            'userFrom': toto.toJson(),
            'userTo': titi.toJson(),
            'isAMessageFromMe': False
        }
        assert message.toJson(userRequester=toto) == {
            'id': message.id,
            'readed': False,
            'dateTime': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'body': "My Message",
            'userFrom': toto.toJson(),
            'userTo': titi.toJson(),
            'isAMessageFromMe': True
        }