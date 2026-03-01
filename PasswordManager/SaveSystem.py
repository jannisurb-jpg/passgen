import sqlite3

class SavingSystem:
    def SavePassword(name, username, password, filename, crypto, key):
        encryptedName = crypto.encrypt(name, key)
        encryptedUsername = crypto.encrypt(username, key)
        encryptedPassword = crypto.encrypt(password, key)

        conn = sqlite3.connect("passgensave.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            name TEXT,
            username TEXT,
            password TEXT
            )
            """)
        
        cursor.execute("""
        INSERT INTO entries (name, username, password) VALUES (?, ?, ?)
        """, (str(encryptedName)[1:-1], str(encryptedUsername)[1:-1], str(encryptedPassword)[1:-1]))

        conn.commit()

        conn.close()

        """with open(filename, 'a') as f:
            f.write(str(encryptedName)[1:-1] + '°' + str(encryptedUsername)[1:-1] + '°' + str(encryptedPassword)[1:-1] + '\n')"""

    def LoadValue(filename, crypto, savedName, savedUsernames, savedPasswords, key):
        encryptedName = []
        encryptedUsername = []
        encryptedPasswords = []
        """with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                parts = line.split("°")

                encryptedName.append(parts[0])
                encryptedUsername.append(parts[1])
                encryptedPasswords.append(parts[2])"""
        
        conn = sqlite3.connect("passgensave.db")
        cursor = conn.cursor()


        
        cursor.execute("SELECT name FROM entries")
        for row in cursor.fetchall():
            encryptedName.append(row[0])

        cursor.execute("SELECT username FROM entries")
        for row in cursor.fetchall():
            encryptedUsername.append(row[0])

        cursor.execute("SELECT password FROM entries")
        for row in cursor.fetchall():
            encryptedPasswords.append(row[0])

        #take apart i-name
        i = 0
        individualBytes = []
        for names in encryptedName:
            individualBytes = [int(x.strip()) for x in str(names).split(",")]
            decryptedName = ''.join(crypto.decrypt(individualBytes, key))
            savedName.append(decryptedName)
            i += 1

        #take apart i-username
        i = 0
        individualBytes = []
        for usernames in encryptedUsername:
            individualBytes = [int(x.strip()) for x in str(usernames).split(",")]
            decryptedUsername = ''.join(crypto.decrypt(individualBytes, key))
            savedUsernames.append(decryptedUsername)
            i += 1

        #take apart i-password
        i = 0
        individualBytes = []
        for passwords in encryptedPasswords:
            individualBytes = [int(x.strip()) for x in str(passwords).split(",")]
            decryptedPassword = ''.join(crypto.decrypt(individualBytes, key))
            savedPasswords.append(decryptedPassword)
            i += 1

        return savedName, savedUsernames ,savedPasswords