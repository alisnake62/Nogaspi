from nogaspi.views.messaging.getConversation import getConversation
from test.functionalTest.dbMagement import sqlQuerysWithCommit
from test.functionalTest.flaskManagement import FakeRequest
import pytest

def test_messaging_getConversation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getConversation(FakeRequest({
        "token": "token_toto",
        "idConversation" : 1
    }))
    assert funcRtr['conversation']['messages'][0]['body'] == 'mon beau message'
    assert funcRtr['conversation']['messages'][1]['body'] == 'mon beau message 2'

def test_messaging_getConversation_if_user_is_taker():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getConversation(FakeRequest({
        "token": "token_tata",
        "idConversation" : 1
    }))
    assert funcRtr['conversation']['messages'][0]['body'] == 'mon beau message'
    assert funcRtr['conversation']['messages'][1]['body'] == 'mon beau message 2'

def test_messaging_getConversation_ok_if_donation_is_archived():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '1');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getConversation(FakeRequest({
        "token": "token_toto",
        "idConversation" : 1
    }))
    assert funcRtr['conversation']['messages'][0]['body'] == 'mon beau message'
    assert funcRtr['conversation']['messages'][1]['body'] == 'mon beau message 2'

def test_messaging_getConversation_ok_if_donation_is_expired():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = getConversation(FakeRequest({
        "token": "token_toto",
        "idConversation" : 1
    }))
    assert funcRtr['conversation']['messages'][0]['body'] == 'mon beau message'
    assert funcRtr['conversation']['messages'][1]['body'] == 'mon beau message 2'

def test_messaging_getConversation_if_bad_user():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        getConversation(FakeRequest({
            "token": "token_titi",
            "idConversation" : 1
        }))

def test_messaging_getConversation_if_bad_Conversation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (1, '1', '1', '2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (1, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (2, '1', '1', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 2');",
        "INSERT INTO `message` (`id`, `idConversation`, `toDonator`, `readed`, `dateTime`, `body`) VALUES (3, '1', '0', '0', NOW() - INTERVAL 2 MINUTE, 'mon beau message 3');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        getConversation(FakeRequest({
            "token": "token_toto",
            "idConversation" : 2
        }))
