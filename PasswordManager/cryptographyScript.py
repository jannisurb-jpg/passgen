import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM as nonce

class EncryptionService:

    #Encryption System
    listOfBytes = []
    listOfEnycryptedBytes = []

    keyBytes = []

    def encrypt(text, key):
        global listOfBytes
        global listOfEnycryptedBytes

        listOfBytes = []
        listOfEnycryptedBytes = []
        listOfCharacters = []

        listOfCharacters = list(text)

        nonceVariable = nonce.generate_key(bit_length=256)
        keyWithNonce = hashlib.sha256(key.encode("utf-8") + nonceVariable)
        keyBytesWithNonce = keyWithNonce.digest()

        #convert to bytes
        k = 0
        for i in listOfCharacters:
            char = listOfCharacters[k]
            listOfBytes.append(ord(char))
            k += 1

        #encrypt with key
        j = 0
        for byte in listOfBytes:
            if(j <= len(keyBytesWithNonce) - 1):
                listOfEnycryptedBytes.append(byte ^ keyBytesWithNonce[j % len(keyBytesWithNonce)])

            elif(j >  len(keyBytesWithNonce) - 1):
                j = 0
                listOfEnycryptedBytes.append(byte ^ keyBytesWithNonce[j % len(keyBytesWithNonce)])
            j += 1

        listOfEnycryptedBytesWithNonce = list(nonceVariable)

        for byte in listOfEnycryptedBytes:
            listOfEnycryptedBytesWithNonce.append(byte)

        return listOfEnycryptedBytesWithNonce


    def decrypt(listOfEnycryptedBytes, key):
        #encrypt with key
        listOfDecryptedCharacters = []
        j = 0
        nonceVariableBytes = []

        nonceVariable = bytes(listOfEnycryptedBytes[:32])
        derived_key = hashlib.sha256(
        key.encode("utf-8") + nonceVariable
        ).digest()

        for byte in listOfEnycryptedBytes:
            if (j <= len(listOfEnycryptedBytes) - 1) and j > 31:
                listOfDecryptedCharacters.append(chr(int(byte) ^ derived_key[j % len(derived_key)]))

            elif(j >  len(listOfEnycryptedBytes) - 1) and j > 31:
                j = 0
                listOfDecryptedCharacters.append(chr(int(byte) ^ derived_key[j % len(derived_key)]))
            j += 1

        return listOfDecryptedCharacters