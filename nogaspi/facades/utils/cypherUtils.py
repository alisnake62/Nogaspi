from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import os

def encrypt(message):
    messageBinary = message.encode('utf8')
    
    with open (f"{os.environ['DIRECTORY_ASSET']}rsaKeys/publicKey.pem",'r') as publicKeyFile:
        publicKeyPem = publicKeyFile.read()

    publicKey = RSA.import_key(publicKeyPem)
    encryptor = PKCS1_OAEP.new(publicKey)
    encryptedMessage = encryptor.encrypt(messageBinary)

    return binascii.hexlify(encryptedMessage).decode('ascii')

def decrypt(encryptedMessage):
    encryptedMessage = binascii.unhexlify(encryptedMessage.encode('ascii'))
    
    with open (f"{os.environ['DIRECTORY_ASSET']}rsaKeys/privateKey.pem",'r') as privateKeyFile:
        privateKeyPem = privateKeyFile.read()

    privateKey = RSA.import_key(privateKeyPem)
    decryptor = PKCS1_OAEP.new(privateKey)
    messageBynary = decryptor.decrypt(encryptedMessage)

    return messageBynary.decode("utf8")