import json

class SavingSystem:
    def SavePassword(name, username, password, filename, crypto, key):
        encryptedName = crypto.encrypt(name, key)
        encryptedUsername = crypto.encrypt(username, key)
        encryptedPassword = crypto.encrypt(password, key)

        with open(filename, 'a') as f:
            f.write(str(encryptedName)[1:-1] + '°' + str(encryptedUsername)[1:-1] + '°' + str(encryptedPassword)[1:-1] + '\n')

    def LoadValue(filename, crypto, savedName, savedUsernames, savedPasswords, key):
        encryptedName = []
        encryptedUsername = []
        encryptedPasswords = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                parts = line.split("°")

                encryptedName.append(parts[0])
                encryptedUsername.append(parts[1])
                encryptedPasswords.append(parts[2])

        #take apart i-name
        i = 0
        individualBytes = []
        for names in encryptedName:
            individualBytes = [int(x.strip()) for x in names.split(",")]
            decryptedName = ''.join(crypto.decrypt(individualBytes, key))
            savedName.append(decryptedName)
            i += 1

        #take apart i-username
        i = 0
        individualBytes = []
        for usernames in encryptedUsername:
            individualBytes = [int(x.strip()) for x in usernames.split(",")]
            decryptedUsername = ''.join(crypto.decrypt(individualBytes, key))
            savedUsernames.append(decryptedUsername)
            i += 1

        #take apart i-password
        i = 0
        individualBytes = []
        for passwords in encryptedPasswords:
            individualBytes = [int(x.strip()) for x in passwords.split(",")]
            decryptedPassword = ''.join(crypto.decrypt(individualBytes, key))
            savedPasswords.append(decryptedPassword)
            i += 1

        return savedName, savedUsernames ,savedPasswords