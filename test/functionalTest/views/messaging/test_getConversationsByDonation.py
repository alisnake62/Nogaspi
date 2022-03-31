from nogaspi.views.messaging.getConversationsByDonation import getConversationsByDonation
from test.functionalTest.dbMagement import sqlQuerysWithCommit
from test.functionalTest.flaskManagement import FakeRequest
import pytest

encryptedMessage1 = f"[\\\"{pytest.encryptedMessage1}\\\"]"
encryptedMessage2 = f"[\\\"{pytest.encryptedMessage2}\\\"]"
encryptedMessage12 = f"[\\\"{pytest.encryptedMessage1}\\\",\\\"{pytest.encryptedMessage2}\\\"]"

def test_messaging_getConversationsByDonation1():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '1', '3');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getConversationsByDonation(FakeRequest({
        "token": "token_toto",
        "idDonation" : 1
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [1, 3]

def test_messaging_getConversationsByDonation2():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '1', '3');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getConversationsByDonation(FakeRequest({
        "token": "token_toto",
        "idDonation" : 2
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [2]

def test_messaging_getConversationsByDonation_sorted_by_last_message():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '1', '3');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 1 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getConversationsByDonation(FakeRequest({
        "token": "token_toto",
        "idDonation" : 1
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [3, 1]

def test_messaging_getConversationsByDonation_with_bad_user():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '1', '3');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        getConversationsByDonation(FakeRequest({
            "token": "token_titi",
            "idDonation" : 2
        }))


def test_messaging_getConversationsByDonation_with_bad_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '1', '3');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        getConversationsByDonation(FakeRequest({
            "token": "token_toto",
            "idDonation" : 3
        }))

def test_messaging_getConversationsByDonation_if_donation_is_expired():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '1', '3');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getConversationsByDonation(FakeRequest({
        "token": "token_toto",
        "idDonation" : 1
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [1, 3]

def test_messaging_getConversationsByDonation_if_donation_is_archived():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '1', '3');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getConversationsByDonation(FakeRequest({
        "token": "token_toto",
        "idDonation" : 1
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [1, 3]