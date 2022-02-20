from nogaspi.views.register.login import User
from nogaspi.views.messaging.initiateConversation import Message, Conversation
from nogaspi.views.food.getDonations import Donation
from nogaspi.dbEngine import EngineSQLAlchemy
from datetime import datetime

def test_conversation_toJson():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        conversation = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message1 = Message(conversation=conversation, toDonator=True, body="My Message 1")
        message1.dateTime = datetime(year=2122, month=1, day=1)
        message2 = Message(conversation=conversation, toDonator=True, body="My Message 1")
        message2.dateTime = datetime(year=2122, month=1, day=2)
        session.add(toto)
        session.add(titi)
        session.add(donation)
        session.add(conversation)
        session.add(message1)
        session.add(message2)
        session.commit()

        assert conversation.toJson(userRequester=titi) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': False,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(titi),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'messages': [message1.toJson(titi), message2.toJson(titi)],
            'donationIsExpired': False,
            'donationIsArchived': False,
            'donationIsValide': True
        }
        assert conversation.toJson(userRequester=toto) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': True,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(toto),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'messages': [message1.toJson(toto), message2.toJson(toto)],
            'donationIsExpired': False,
            'donationIsArchived': False,
            'donationIsValide': True
        }
        assert conversation.toJsonlight(userRequester=titi) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': False,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(titi),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'donationIsExpired': False,
            'donationIsArchived': False,
            'donationIsValide': True
        }
        assert conversation.toJsonlight(userRequester=toto) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': True,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(toto),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'donationIsExpired': False,
            'donationIsArchived': False,
            'donationIsValide': True
        }

def test_conversation_toJson_with_one_message():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        conversation = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message = Message(conversation=conversation, toDonator=True, body="My Message 1")
        message.dateTime = datetime(year=2122, month=1, day=1)
        session.add(titi)
        session.add(donation)
        session.add(conversation)
        session.add(message)
        session.commit()

        assert conversation.toJson(userRequester=titi) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': False,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message.toJson(titi),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'messages': [message.toJson(titi)],
            'donationIsExpired': False,
            'donationIsArchived': False,
            'donationIsValide': True
        }
        assert conversation.toJson(userRequester=toto) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': True,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message.toJson(toto),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'messages': [message.toJson(toto)],
            'donationIsExpired': False,
            'donationIsArchived': False,
            'donationIsValide': True
        }
        assert conversation.toJsonlight(userRequester=titi) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': False,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message.toJson(titi),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'donationIsExpired': False,
            'donationIsArchived': False,
            'donationIsValide': True
        }
        assert conversation.toJsonlight(userRequester=toto) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': True,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message.toJson(toto),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'donationIsExpired': False,
            'donationIsArchived': False,
            'donationIsValide': True
        }

def test_conversation_toJson_with_expired_donation():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2022, month=1, day=1))
        conversation = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message1 = Message(conversation=conversation, toDonator=True, body="My Message 1")
        message1.dateTime = datetime(year=2122, month=1, day=1)
        message2 = Message(conversation=conversation, toDonator=True, body="My Message 1")
        message2.dateTime = datetime(year=2122, month=1, day=2)
        session.add(toto)
        session.add(titi)
        session.add(donation)
        session.add(conversation)
        session.add(message1)
        session.add(message2)
        session.commit()

        assert conversation.toJson(userRequester=titi) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': False,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(titi),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'messages': [message1.toJson(titi), message2.toJson(titi)],
            'donationIsExpired': True,
            'donationIsArchived': False,
            'donationIsValide': False
        }
        assert conversation.toJson(userRequester=toto) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': True,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(toto),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'messages': [message1.toJson(toto), message2.toJson(toto)],
            'donationIsExpired': True,
            'donationIsArchived': False,
            'donationIsValide': False
        }
        assert conversation.toJsonlight(userRequester=titi) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': False,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(titi),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'donationIsExpired': True,
            'donationIsArchived': False,
            'donationIsValide': False
        }
        assert conversation.toJsonlight(userRequester=toto) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': True,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(toto),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'donationIsExpired': True,
            'donationIsArchived': False,
            'donationIsValide': False
        }

def test_conversation_toJson_with_archived_donation():
    with EngineSQLAlchemy() as session:
        toto = User("toto@toto.fr", "toto_password", "toto", "image_toto.jpg")
        titi = User("titi@titi.fr", "titi_password", "titi", "image_titi.jpg")
        donation = Donation(toto, 45, 3, 500, datetime(year=2122, month=1, day=1))
        donation.archive = 1
        conversation = Conversation(donation=donation, userDonator=toto, userTaker=titi)
        message1 = Message(conversation=conversation, toDonator=True, body="My Message 1")
        message1.dateTime = datetime(year=2122, month=1, day=1)
        message2 = Message(conversation=conversation, toDonator=True, body="My Message 1")
        message2.dateTime = datetime(year=2122, month=1, day=2)
        session.add(toto)
        session.add(titi)
        session.add(donation)
        session.add(conversation)
        session.add(message1)
        session.add(message2)
        session.commit()

        assert conversation.toJson(userRequester=titi) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': False,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(titi),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'messages': [message1.toJson(titi), message2.toJson(titi)],
            'donationIsExpired': False,
            'donationIsArchived': True,
            'donationIsValide': False
        }
        assert conversation.toJson(userRequester=toto) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': True,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(toto),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'messages': [message1.toJson(toto), message2.toJson(toto)],
            'donationIsExpired': False,
            'donationIsArchived': True,
            'donationIsValide': False
        }
        assert conversation.toJsonlight(userRequester=titi) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': False,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(titi),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'donationIsExpired': False,
            'donationIsArchived': True,
            'donationIsValide': False
        }
        assert conversation.toJsonlight(userRequester=toto) == {
            'id': conversation.id,
            'idDonation': donation.id,
            'isMyDonation': True,
            'dateBeginning': int(datetime.timestamp(datetime(year=2122, month=1, day=1))),
            'lastMessage': message2.toJson(toto),
            'userDonator': toto.toJson(),
            'userTaker': titi.toJson(),
            'donationIsExpired': False,
            'donationIsArchived': True,
            'donationIsValide': False
        }