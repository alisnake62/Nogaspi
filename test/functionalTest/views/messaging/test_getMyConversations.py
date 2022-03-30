from nogaspi.views.messaging.getMyConversations import getMyConversations
from test.functionalTest.dbMagement import sqlQuerysWithCommit
from test.functionalTest.flaskManagement import FakeRequest
import pytest

encryptedMessage1 = f"[\\\"{pytest.encryptedMessage1}\\\"]"
encryptedMessage2 = f"[\\\"{pytest.encryptedMessage2}\\\"]"
encryptedMessage12 = f"[\\\"{pytest.encryptedMessage1}\\\",\\\"{pytest.encryptedMessage2}\\\"]"

def test_messaging_getMyConversations1():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getMyConversations(FakeRequest({
        "token": "token_toto",
        "withArchivedDonations": '0',
        "withExpiredDonations": '0'
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [1, 2, 3]

def test_messaging_getMyConversations2():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '1', '3');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getMyConversations(FakeRequest({
        "token": "token_tata",
        "withArchivedDonations": '0',
        "withExpiredDonations": '0'
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [1, 2]

def test_messaging_getMyConversations_with_bad_user():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getMyConversations(FakeRequest({
        "token": "token_titi",
        "withArchivedDonations": '0',
        "withExpiredDonations": '0'
    }))
    assert [c['id'] for c in funcRtr['conversations']] == []

def test_messaging_getMyConversations_with_archived_donation1():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '1');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getMyConversations(FakeRequest({
        "token": "token_toto",
        "withArchivedDonations": '0',
        "withExpiredDonations": '0'
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [2]

def test_messaging_getMyConversations_with_archived_donation2():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '1');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getMyConversations(FakeRequest({
        "token": "token_toto",
        "withArchivedDonations": '1',
        "withExpiredDonations": '0'
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [1, 2, 3]

def test_messaging_getMyConversations_with_expired_donation1():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getMyConversations(FakeRequest({
        "token": "token_toto",
        "withArchivedDonations": '0',
        "withExpiredDonations": '0'
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [2]

def test_messaging_getMyConversations_with_expired_donation2():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage1}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage2}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');",
        f"INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, '{encryptedMessage12}');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getMyConversations(FakeRequest({
        "token": "token_toto",
        "withArchivedDonations": '0',
        "withExpiredDonations": '1'
    }))
    assert [c['id'] for c in funcRtr['conversations']] == [1, 2, 3]