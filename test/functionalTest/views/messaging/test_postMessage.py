from nogaspi.views.messaging.postMessage import postMessage
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_messaging_postMessage1():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = postMessage(FakeRequest({
        "token": "token_tata",
        "idConversation" : 1,
        "body": "Mon beau Message 5"
    }))
    assert funcRtr['posted']
    assert len(sqlSelect(table='conversation')) == 3
    assert len(sqlSelect(table='message')) == 5
    assert sqlSelect(table='message', conditions="WHERE body = 'Mon beau Message 5'")[0]['idConversation'] == 1
    assert sqlSelect(table='message', conditions="WHERE body = 'Mon beau Message 5'")[0]['toDonator'] == 1
    assert sqlSelect(table='message', conditions="WHERE body = 'Mon beau Message 5'")[0]['readed'] == 0

def test_messaging_postMessage2():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = postMessage(FakeRequest({
        "token": "token_toto",
        "idConversation" : 1,
        "body": "Mon beau Message 5"
    }))
    assert funcRtr['posted']
    assert len(sqlSelect(table='conversation')) == 3
    assert len(sqlSelect(table='message')) == 5
    assert sqlSelect(table='message', conditions="WHERE body = 'Mon beau Message 5'")[0]['idConversation'] == 1
    test = sqlSelect(table='message', conditions="WHERE body = 'Mon beau Message 5'")[0]
    assert sqlSelect(table='message', conditions="WHERE body = 'Mon beau Message 5'")[0]['toDonator'] == 0
    assert sqlSelect(table='message', conditions="WHERE body = 'Mon beau Message 5'")[0]['readed'] == 0

def test_messaging_postMessage_with_bad_user():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        postMessage(FakeRequest({
            "token": "token_titi",
            "idConversation" : 1,
            "body": "Mon beau Message 5"
        }))

def test_messaging_postMessage_with_bad_conversation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        postMessage(FakeRequest({
            "token": "token_tata",
            "idConversation" : 4,
            "body": "Mon beau Message 5"
        }))

def test_messaging_postMessage_with_archived_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '1');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        postMessage(FakeRequest({
            "token": "token_tata",
            "idConversation" : 1,
            "body": "Mon beau Message 5"
        }))

def test_messaging_postMessage_with_expired_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (2, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (3, '1', '2', '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '2', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '2', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (4, '3', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        postMessage(FakeRequest({
            "token": "token_tata",
            "idConversation" : 1,
            "body": "Mon beau Message 5"
        }))