from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import os

def getEncryptor():
    with open (f"{os.environ['DIRECTORY_PROJECT']}assets/rsaKeys/publicKey.pem",'r') as publicKeyFile:
        publicKeyPem = publicKeyFile.read()

    publicKey = RSA.import_key(publicKeyPem)

    return PKCS1_OAEP.new(publicKey)

def getDecryptor():
    with open (f"{os.environ['DIRECTORY_PROJECT']}assets/rsaKeys/privateKey.pem",'r') as privateKeyFile:
        privateKeyPem = privateKeyFile.read()

    privateKey = RSA.import_key(privateKeyPem)

    return PKCS1_OAEP.new(privateKey)

def encrypt(encryptor, message):
    messageBinary = message.encode('utf8')
    encryptedMessage = encryptor.encrypt(messageBinary)

    return binascii.hexlify(encryptedMessage).decode('ascii')

def decrypt(decryptor, encryptedMessage):
    encryptedMessage = binascii.unhexlify(encryptedMessage.encode('ascii'))
    messageBynary = decryptor.decrypt(encryptedMessage)

    return messageBynary.decode("utf8")