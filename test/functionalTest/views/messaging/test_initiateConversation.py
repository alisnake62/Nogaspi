from nogaspi.views.messaging.initiateConversation import initiateConversation
from test.functionalTest.dbMagement import sqlQuerysWithCommit, sqlSelect
from test.functionalTest.flaskManagement import FakeRequest
import pytest
import json

def test_messaging_initiateConversation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = initiateConversation(FakeRequest({
        "token": "token_tata",
        "idDonation" : 1,
        "firstMessage": "Mon beau Message"
    }))
    assert funcRtr['isInitiate']
    assert len(sqlSelect(table='conversation')) == 1
    assert len(sqlSelect(table='message')) == 1
    assert sqlSelect(table='conversation')[0]['idDonation'] == 1
    assert sqlSelect(table='conversation')[0]['idUserDonator'] == 1
    assert sqlSelect(table='conversation')[0]['idUserTaker'] == 2
    assert sqlSelect(table='message')[0]['idConversation'] == sqlSelect(table='conversation')[0]['id']
    assert sqlSelect(table='message')[0]['toDonator'] == 1
    assert sqlSelect(table='message')[0]['readed'] == 0
    assert type(json.loads(sqlSelect(table='message')[0]['body'])) == list

def test_messaging_initiateConversation_if_conversation_already_exist_with_other_user():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (3, 'titi@titi.fr', 'titi', 'titi', NULL, 'token_titi', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '1', '1', '3');",
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = initiateConversation(FakeRequest({
        "token": "token_tata",
        "idDonation" : 1,
        "firstMessage": "Mon beau Message"
    }))
    assert funcRtr['isInitiate']
    assert len(sqlSelect(table='conversation')) == 2
    assert len(sqlSelect(table='message')) == 1
    assert sqlSelect(table='conversation', conditions="WHERE idUserTaker = 2")[0]['idDonation'] == 1
    assert sqlSelect(table='conversation', conditions="WHERE idUserTaker = 2")[0]['idUserDonator'] == 1
    assert sqlSelect(table='message')[0]['idConversation'] == sqlSelect(table='conversation', conditions="WHERE idUserTaker = 2")[0]['id']
    assert sqlSelect(table='message')[0]['toDonator'] == 1
    assert sqlSelect(table='message')[0]['readed'] == 0
    assert type(json.loads(sqlSelect(table='message')[0]['body'])) == list

def test_messaging_initiateConversation_with_long_message():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    funcRtr = initiateConversation(FakeRequest({
        "token": "token_tata",
        "idDonation" : 1,
        "firstMessage": "Mon beau MessageMon beau MessageMon beau MessageMon beau MessageMon beau MessageMon beau MessageMon beau MessageMon beau Message"
    }))
    assert funcRtr['isInitiate']
    assert len(sqlSelect(table='conversation')) == 1
    assert len(sqlSelect(table='message')) == 1
    assert sqlSelect(table='conversation')[0]['idDonation'] == 1
    assert sqlSelect(table='conversation')[0]['idUserDonator'] == 1
    assert sqlSelect(table='conversation')[0]['idUserTaker'] == 2
    assert sqlSelect(table='message')[0]['idConversation'] == sqlSelect(table='conversation')[0]['id']
    assert sqlSelect(table='message')[0]['toDonator'] == 1
    assert sqlSelect(table='message')[0]['readed'] == 0
    assert type(json.loads(sqlSelect(table='message')[0]['body'])) == list
    assert len(json.loads(sqlSelect(table='message')[0]['body'])) == 2


def test_messaging_initiateConversation_if_conversation_already_exist_with_your_user():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');",
        "INSERT INTO `conversation` (`id`, `idDonation`, `idUserDonator`, `idUserTaker`) VALUES (2, '1', '1', '2');",
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        initiateConversation(FakeRequest({
            "token": "token_tata",
            "idDonation" : 1,
            "firstMessage": "Mon beau Message"
        }))

def test_messaging_initiateConversation_with_my_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        initiateConversation(FakeRequest({
            "token": "token_toto",
            "idDonation" : 1,
            "firstMessage": "Mon beau Message"
        }))

def test_messaging_initiateConversation_with_bad_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        initiateConversation(FakeRequest({
            "token": "token_tata",
            "idDonation" : 2,
            "firstMessage": "Mon beau Message"
        }))

def test_messaging_initiateConversation_with_archived_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW(), NOW() + INTERVAL 1 DAY, NULL, '1');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        initiateConversation(FakeRequest({
            "token": "token_tata",
            "idDonation" : 1,
            "firstMessage": "Mon beau Message"
        }))

def test_messaging_initiateConversation_with_expired_donation():
    querys = [
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (1, 'toto@toto.fr', 'toto', 'toto', NULL, 'token_toto', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `userNogaspi` (`id`, `mail`, `password`, `pseudo`, `profilePicture`, `token`, `token_expiration`, `points`) VALUES (2, 'tata@tata.fr', 'tata', 'tata', NULL, 'token_tata', NOW() + INTERVAL 1 DAY, '0');",
        "INSERT INTO `donation` (`id`, `idUser`, `latitude`, `longitude`, `geoPrecision`, `startingDate`, `endingDate`, `idDonationCode`, `archive`) VALUES (1, '1', '40', '40', '500', NOW() - INTERVAL 2 DAY, NOW() - INTERVAL 1 DAY, NULL, '0');"
    ]
    sqlQuerysWithCommit(querys)
    
    with pytest.raises(Exception):
        initiateConversation(FakeRequest({
            "token": "token_tata",
            "idDonation" : 1,
            "firstMessage": "Mon beau Message"
        }))