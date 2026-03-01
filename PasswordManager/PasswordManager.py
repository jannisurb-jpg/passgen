import tkinter as tk
import random
import string
import pyperclip
import ast
import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM as nonce

#Save System
fileName = "PassGenSave.txt"

savedPasswords = []
savedUsernames = []
savedName = []
savedNamesEncrypted = []
howManySaves = 0

#Encryption System
listOfBytes = []
listOfEnycryptedBytes = []

key = "DeGNPG_eD}*5tx9L;sSf-ku;:[dh1hp5LHR`=ZW7Cqa%mO9Nh"
#keyBytes = [68, 101, 71, 78, 80, 71, 95, 101, 68, 125, 42, 53, 116, 120, 57, 76, 59, 115, 83, 102, 45, 107, 117, 59, 58, 91, 100, 104, 49, 104, 112, 53, 76, 72, 82, 96, 61, 90, 87, 55, 67, 113, 97, 37, 109, 79, 57, 78, 104]
keyBytes = []

def encrypt(text):
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


def decrypt(listOfEnycryptedBytes):
    #encrypt with key
    listOfDecryptedCharacters = []
    j = 0
    nonceVariableBytes = []

    nonceVariable = bytes(listOfEnycryptedBytes[:32])
    print("NonceVariable: ", nonceVariable)
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



def SavePassword(name, username, password, filename):
    encryptedName = encrypt(name)
    encryptedUsername = encrypt(username)
    encryptedPassword = encrypt(password)

    with open(filename, 'a') as f:
        f.write(str(encryptedName)[1:-1] + '°' + str(encryptedUsername)[1:-1] + '°' + str(encryptedPassword)[1:-1] + '\n')

def LoadValue(filename):
    global howManySaves
    global savedName
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
        decryptedName = ''.join(decrypt(individualBytes))
        savedName.append(decryptedName)
        i += 1

    #take apart i-username
    i = 0
    individualBytes = []
    for usernames in encryptedUsername:
        individualBytes = [int(x.strip()) for x in usernames.split(",")]
        decryptedUsername = ''.join(decrypt(individualBytes))
        savedUsernames.append(decryptedUsername)
        i += 1

    #take apart i-password
    i = 0
    individualBytes = []
    for passwords in encryptedPasswords:
        individualBytes = [int(x.strip()) for x in passwords.split(",")]
        decryptedPassword = ''.join(decrypt(individualBytes))
        savedPasswords.append(decryptedPassword)
        i += 1

def GenerateRandomPassoword():
    #Set and reset properties for the new password
    desiredPasswordLength = int(slider.get()) + 1
    currentPassword = ""

    #generate password
    i = 0
    for i in range(1, desiredPasswordLength):
        currentPassword += str(random.choice(all_char))
        i += 1
    label.config(text=currentPassword)

def UseDigits():
    global all_char
    noDigits = []

    if usedigits.get():
        all_char += string.digits
    else:
        for i in all_char:
            if not i.isdigit():
                noDigits.append(i)
        
        all_char = noDigits
    checkIfEnoughConditionsForPassword()

def UsePunctuations():
    global all_char
    noPuncs = []

    if usePunctuations.get():
        all_char += string.punctuation
    else:
        for i in all_char:
            if not i in string.punctuation:
                noPuncs.append(i)
        
        all_char = noPuncs
    checkIfEnoughConditionsForPassword()

def UseUpperCase():
    global all_char
    noUpperCase = []

    if useUppercase.get():
        all_char += string.ascii_uppercase
    else:
        for i in all_char:
            if not i in string.ascii_uppercase:
                noUpperCase.append(i)
        
        all_char = noUpperCase
    checkIfEnoughConditionsForPassword()

def UseLowerCase():
    global all_char
    noLowerCase = []

    if useLowercase.get():
        all_char += string.ascii_lowercase
    else:
        for i in all_char:
            if not i in string.ascii_lowercase:
                noLowerCase.append(i)
        
        all_char = noLowerCase
    checkIfEnoughConditionsForPassword()

def checkIfEnoughConditionsForPassword():
    #if atleast 2 are active you can check whatever you want
    if sum([useLowercase.get(), usedigits.get(), usePunctuations.get(), useUppercase.get()]) >= 2:
        if useLowercase.get():
            checkboxForLowercase.config(state="active")
        if useUppercase.get():
            checkboxForUppercase.config(state="active")
        if usedigits.get():
            checkboxForDigits.config(state="active")
        if usePunctuations.get():
            checkboxForPunctuations.config(state="active")
    #if only one is active disable this one
    else:
        if useLowercase.get():
            checkboxForLowercase.config(state="disabled")
        if useUppercase.get():
            checkboxForUppercase.config(state="disabled")
        if usedigits.get():
            checkboxForDigits.config(state="disabled")
        if usePunctuations.get():
            checkboxForPunctuations.config(state="disabled")

def copy():
    global currentPassword
    pyperclip.copy(label.cget("text"))

def Save():
    SavePassword(str(nameInput.get()), str(usernameInput.get()), str(label.cget("text")), fileName)

def Load():
    LoadValue(fileName)
    """print("Names: ")
    for names in savedName:
        print(names)
    
    print("Usernames: ")
    for usernames in savedUsernames:
        print(usernames)
    
    print("Passwords: ")
    for passwords in savedPasswords:
        print(passwords)"""

def OpenCreateMenu():
    pass

def OpenEntry(whichButtonAsInteger):
    global currentSite
    currentSite = 1
    for element in entriesUI:
        element.grid_forget()

    text = "Name: " + savedName[whichButtonAsInteger] + "\nUsername: " + savedUsernames[whichButtonAsInteger] + "\nPassword: " + savedPasswords[whichButtonAsInteger]
    
    for element in entryTemplate:
        element.grid(row=0, column=0, sticky="nsew")

        if currentSite == 1:
            element.config(text= text)

        

desiredPasswordLength = 8
currentPassword = "" 
maxPasswordLength = 100
sliderLength = 500
all_char = string.ascii_letters + string.digits + string.punctuation
uiColorCode = "#87CEEB"
backgroundColor = "#353535"
textColor = "#FFFFFF"
rowsPerSide = 10

#Only allow digits in the input field
def only_digits(P):
    return P.isdigit() or P == ""

#entry password with hash
entryPassword = input("Enter Password here: ") #.encode('utf-8')
#entryPassword = hashlib.sha256(entryPassword).hexdigest()
key = entryPassword

listOfKeyCharacters = list(key)

j = 0
for i in listOfKeyCharacters:
    char = listOfKeyCharacters[j]
    keyBytes.append(ord(char))
    j += 1

#create the window
root = tk.Tk()
root.title("Password Manager")
root.geometry("500x700")
root.config(bg=backgroundColor)

# Specify Grid
root.grid_columnconfigure(0, weight=1)


#create the bools for checkboxes
usedigits = tk.BooleanVar(value=True)
usePunctuations = tk.BooleanVar(value=True)
useUppercase = tk.BooleanVar(value=True)
useLowercase = tk.BooleanVar(value=True)

#convert so we can use the only digits
vcmd = root.register(only_digits)

#create all the UI
#create the inputfield
slider = tk.Scale(root, from_=1, to_=maxPasswordLength, orient="horizontal",length=sliderLength,background=uiColorCode,foreground=textColor)
slider.grid(row=3, column=0)

#create the Input for the name
nameInput = tk.Entry(root)
nameInput.grid(row=0,column=0)

#create usernameEntry
usernameInput = tk.Entry(root)
usernameInput.grid(row=1, column=0)

#create the output label
label = tk.Label(root, text="Your password:",background=uiColorCode,foreground=textColor)
label.grid(row=2,column=0)

#create button for password creation
generateButton = tk.Button(root, bg= uiColorCode, text= 'Generate Password', command=GenerateRandomPassoword,foreground=textColor)
generateButton.grid(row=4,column=0)

#Clipboard Button
clipboardButton = tk.Button(root, bg= uiColorCode, text= 'Copy', command=copy,foreground=textColor)
clipboardButton.grid(row=9,column=0)

#save button
saveButton = tk.Button(root, bg= uiColorCode, text= 'Save', command=Save,foreground=textColor)
saveButton.grid(row=10,column=0)

#test load button
loadButton = tk.Button(root, bg= uiColorCode, text= 'Load', command=Load,foreground=textColor)
loadButton.grid(row=11,column=0)

#create the checkboxes for enableing digits, punctuations and letters small and big
checkboxForDigits = tk.Checkbutton(root, text="Use digits", command=UseDigits, variable=usedigits)
checkboxForDigits.grid(row=5,column=0)

checkboxForPunctuations = tk.Checkbutton(root, text="Use punctuations", command=UsePunctuations, variable=usePunctuations)
checkboxForPunctuations.grid(row=6,column=0)

checkboxForUppercase = tk.Checkbutton(root, text="Use uppercased lettes", command=UseUpperCase, variable=useUppercase)
checkboxForUppercase.grid(row=7,column=0)

checkboxForLowercase= tk.Checkbutton(root, text="Use lowercased lettes", command=UseLowerCase, variable=useLowercase)
checkboxForLowercase.grid(row=8,column=0)

Load()

#create entries UI
entries = []

l = 0
while l <= len(savedName) - 1:
    newLabel = tk.Button(root, text="Test", command= lambda x=l: OpenEntry(x))
    entries.append(newLabel)
    l += 1
l = 0
for entrie in entries:
    entrie.config(text= savedName[l])
    entrie.grid(row=l, column=0, sticky="nsew")
    l += 1

for l in range(len(entries)):
    if l <= rowsPerSide:
        root.grid_rowconfigure(l, weight=1)
    else:
        root.grid_rowconfigure(l, weight=0)

#create plus button
createEntryButton = tk.Button(root, text="+", compound="center", width=5, height=3)
if(len(entries) - 1 <= rowsPerSide):
    createEntryButton.grid(row=len(entries) - 1, column= 0, sticky = "se", padx=5, pady=5)
else:
    createEntryButton.grid(row=rowsPerSide, column= 0, sticky = "se", padx=5, pady=5)

#create Entryapge
entryText = tk.Label(root)

createEntryUI = [slider, nameInput, usernameInput, label, generateButton, clipboardButton, saveButton, loadButton, checkboxForDigits, checkboxForPunctuations, checkboxForLowercase, checkboxForUppercase]
entriesUI = []
entryTemplate = [entryText]

for element in entries:
    entriesUI.append(element)

for element in createEntryUI:
    element.grid_forget()

root.mainloop()