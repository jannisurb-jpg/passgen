import os
import hashlib
import sqlite3

listOfBytes = []
listOfEnycryptedBytes = []

whatAction = input("encrypt/decrypt?")

key = "DeGNPG_eD}*5tx9L;sSf-ku;:[dh1hp5LHR`=ZW7Cqa%mO9Nh"
keyBytes = [68, 101, 71, 78, 80, 71, 95, 101, 68, 125, 42, 53, 116, 120, 57, 76, 59, 115, 83, 102, 45, 107, 117, 59, 58, 91, 100, 104, 49, 104, 112, 53, 76, 72, 82, 96, 61, 90, 87, 55, 67, 113, 97, 37, 109, 79, 57, 78, 104]

#Just one time for key
#listOfKeyCharacters = list(key)
#
#j = 0
#for i in listOfKeyCharacters:
    #char = listOfKeyCharacters[j]
    #keyBytes.append(ord(char))
    #j += 1
#print(keyBytes)


def encrypt(text):
    global listOfBytes
    listOfCharacters = list(text)

    #convert to bytes
    k = 0
    for i in listOfCharacters:
        char = listOfCharacters[k]
        listOfBytes.append(ord(char))
        k += 1

    #encrypt with key
    j = 0
    for byte in listOfBytes:
        if(j <= len(keyBytes) - 1):
            listOfEnycryptedBytes.append((byte ^ keyBytes[j % len(keyBytes)]))

        elif(j > len(keyBytes) - 1):
            j = 0
            listOfEnycryptedBytes.append((byte ^ keyBytes[j % len(keyBytes)]))
        j += 1
    print(listOfEnycryptedBytes)

def decrypt(text):
    #encrypt with key
    text = text.replace("[", "")
    text = text.replace("]", "")
    listOfEnycryptedBytes = text.split(",")
    listOfDecryptedCharacters = []
    j = 0
    for byte in listOfEnycryptedBytes:
        if(j <= len(keyBytes) - 1):
            listOfDecryptedCharacters.append(chr((int(byte) ^ keyBytes[j % len(keyBytes)])))

        elif(j > len(keyBytes) - 1):
            j = 0
            listOfDecryptedCharacters.append(chr((int(byte) ^ keyBytes[j % len(keyBytes)])))
        j += 1

    print(''.join(str(x) for x in listOfDecryptedCharacters))


if(whatAction == "encrypt"):
    text = input("Which word?")
    encrypt(text)

elif(whatAction == "decrypt"):
    text = input("Which Cryptionfile?")
    decrypt(text)