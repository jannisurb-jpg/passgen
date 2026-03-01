from cryptographyScript import EncryptionService
from SaveSystem import SavingSystem
import string
import pyperclip
import tkinter as tk
from tkinter import font
import random
import math

fileName = "PassGenSave.txt"
savedNames = []
savedUsernames = []
savedPasswords = []

desiredPasswordLength = 8
currentPassword = "" 
maxPasswordLength = 100
sliderLength = 500
all_char = string.ascii_letters + string.digits + string.punctuation
uiColorCode = "#87CEEB"
uiWhiteColor = "#FFFFFF"
backgroundColor = "#353535"
textColor = "#FFFFFF"
textColor2 = "#000000"
rowsPerSide = 10
borderSize = 2
wrapLengthForEntryTemplate = 500

def StartLoadingData():
    global savedNames
    global savedUsernames
    global savedPasswords
    global howManySides
    savedNames, savedUsernames, savedPasswords = SavingSystem.LoadValue(fileName, EncryptionService, savedNames, savedUsernames, savedPasswords, key)

    howManySides = int(math.ceil(len(savedNames)/rowsPerSide))


key = input("Enter Password here: ")
StartLoadingData()

#Here starts the GUIHandler
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

def OpenCreateMenu():
    #Remove the unnecessary UI
    createEntryButton.grid_remove()

    for element in entryTemplate:
        element.grid_remove()

    for i,element in enumerate(entriesUI):
        element.grid_remove()
        root.grid_rowconfigure(i, weight=0)

    #Show the creating UI
    root.grid_columnconfigure(1, weight=1)

    for l, element in enumerate(createEntryUI):
        if l == 8 or l == 10:
            element.grid(column=1)
        else:
            element.grid(column=0)
        
        if l <= 9:
            root.grid_rowconfigure(l, weight=1)

def OpenEntriesView():
    #Reload all data
    global savedNames
    global savedUsernames
    global savedPasswords
    global currentSite
    global howManySides
    currentSite = 1
    savedNames = []
    savedUsernames = []
    savedPasswords = []

    StartLoadingData()

    #create new Buttons for new Data
    l = len(entries)
    while l <= len(savedNames) - 1:
        newLabel = tk.Button(root, text=savedNames[l], command= lambda x=l: OpenEntry(x), borderwidth=borderSize)
        entries.append(newLabel)
        entriesUI.append(newLabel)
        l += 1

    #sort alphabetically
    entriesUI.sort(key=lambda b: b.cget("text").lower())

    #Remove the unnecessary UI
    for l, element in enumerate(entryTemplate):
        element.grid_remove()
        root.grid_rowconfigure(l, weight=0)

    for l, element in enumerate(createEntryUI):
        element.grid_remove()
        root.grid_rowconfigure(l, weight=0)

    root.grid_columnconfigure(1, weight=0)

    #Show entriesUI
    for l,element in enumerate(entriesUI):
        if(l < rowsPerSide):
            element.grid(sticky="nsew")
            root.grid_rowconfigure(l, weight=1)
        elif(l == rowsPerSide):
            sideSelectionFrame.grid(row=l, column=0, sticky="nsew")

            #create the grid for the side selection
            i = 0
            while i <= howManySides - 1:
                sideSelectionFrame.grid_columnconfigure(i, weight=1)
                sideSelectionButton[i].grid(row=0,column=i)
                i += 1

            root.grid_rowconfigure(l, weight=1)

    if(len(entries) - 1 <= rowsPerSide):
        createEntryButton.grid(row=len(entriesUI) - 1, column= 0, sticky = "se", padx=5, pady=5)
    else:
        createEntryButton.grid(row=rowsPerSide - 1, column= 0, sticky = "se", padx=5, pady=5)

def OpenEntry(whichButtonAsInteger):
    global currentSite
    currentSite = 1

    text = "Name: " + savedNames[whichButtonAsInteger] + "\nUsername: " + savedUsernames[whichButtonAsInteger] + "\nPassword: " + savedPasswords[whichButtonAsInteger]

    #Remove the unnecessary UI
    for l,element in enumerate(entriesUI):
        element.grid_remove()
        root.grid_rowconfigure(l, weight=0)

    createEntryButton.grid_forget()
    
    #Show the EntryUI + create button
    root.grid_columnconfigure(1, weight=0)
    root.grid_rowconfigure(0, weight=1)
    createEntryButton.grid(row=0, column= 0, sticky = "se", padx=5, pady=5)

    for element in entryTemplate:
        element.grid(row=0, column=0, sticky="nsew")

        if currentSite == 1:
            element.config(text= text)
    
    createEntryButton.lift()

def OpenSide(whichSideToOpen):
    global currentSite
    currentSite = whichSideToOpen
    print("Opening side: ", currentSite)

    #Show entriesUI
    #calculate which entries to show on which side
    maxElementInEntriesUI = currentSite + 1 * rowsPerSide
    minElementInEntriesUI = currentSite * rowsPerSide

    #remove the last side
    for l, element in enumerate(entriesUI):
        if(l <= minElementInEntriesUI + 1):
            element.grid_remove()

    l = minElementInEntriesUI
    for element in entriesUI:
        if(l < maxElementInEntriesUI):
            element.grid(sticky="nsew")
            root.grid_rowconfigure(l - minElementInEntriesUI, weight=1)
        elif(l == maxElementInEntriesUI):
            sideSelectionFrame.grid(row=l, column=0, sticky="nsew")

            #create the grid for the side selection
            i = 0
            while i <= howManySides - 1:
                sideSelectionFrame.grid_columnconfigure(i, weight=1)
                sideSelectionButton[i].grid(row=0,column=i)
                i += 1

            root.grid_rowconfigure(l, weight=1)
        l += 1

    if(len(entries) - 1 <= rowsPerSide):
        createEntryButton.grid(row=len(entriesUI) - 1, column= 0, sticky = "se", padx=5, pady=5)
    else:
        createEntryButton.grid(row=rowsPerSide - 1, column= 0, sticky = "se", padx=5, pady=5)



def Load():
    savedNames, savedUsernames, savedPasswords = SavingSystem.LoadValue(fileName, EncryptionService, savedNames, savedUsernames, savedPasswords, key)

def Save():
    SavingSystem.SavePassword(str(nameInput.get()), str(usernameInput.get()), str(label.cget("text")), fileName, EncryptionService, key)

def resize(event):
    if event.width > 100:
        entryText.config(wraplength=event.width - 40)
        label.config(wraplength=event.width - 40)

#create the window
root = tk.Tk()
root.title("Password Manager")
root.geometry("500x700")
root.minsize(400, 560)
root.config(bg=backgroundColor)

#add frame for side selection
sideSelectionFrame = tk.Frame(root, bg=backgroundColor)

# Specify Grid
root.grid_columnconfigure(0, weight=1)

#create the bools for checkboxes
usedigits = tk.BooleanVar(value=True)
usePunctuations = tk.BooleanVar(value=True)
useUppercase = tk.BooleanVar(value=True)
useLowercase = tk.BooleanVar(value=True)

#other variables
label_font = font.Font(family="Arial", size=20)

#create all the UI
#create the inputfield
slider = tk.Scale(root, from_=1, to_=maxPasswordLength, background=uiWhiteColor, orient="horizontal",foreground=textColor2, borderwidth=borderSize)
slider.grid(row=3, column=0, columnspan=2, sticky= "nsew")

#create the Input for the name
nameInput = tk.Entry(root, borderwidth=borderSize)
nameInput.grid(row=0,column=0, columnspan=2, sticky= "nsew")

#create usernameEntry
usernameInput = tk.Entry(root, borderwidth=borderSize)
usernameInput.grid(row=1, column=0, columnspan=2, sticky= "nsew")

#create the output label
label = tk.Label(root, text="Your password:",foreground=textColor2, background=uiWhiteColor, borderwidth=borderSize)
label.grid(row=2,column=0,columnspan=2, sticky= "nsew")

#create button for password creation
generateButton = tk.Button(root, bg= uiColorCode, text= 'Generate Password', command=GenerateRandomPassoword,foreground=textColor, borderwidth=borderSize)
generateButton.grid(row=4,column=0, columnspan=2, sticky= "nsew")

#Clipboard Button
clipboardButton = tk.Button(root, bg= uiColorCode, text= 'Copy', command=copy,foreground=textColor, borderwidth=borderSize)
clipboardButton.grid(row=7,column=0, columnspan=2, sticky= "nsew")

#save button
saveButton = tk.Button(root, bg= uiColorCode, text= 'Save', command=Save,foreground=textColor, borderwidth=borderSize)
saveButton.grid(row=8,column=0, columnspan=2, sticky= "nsew")

#back to entriesbutton
backToEntriesButton = tk.Button(root, bg= uiColorCode, text= 'Back', command=OpenEntriesView,foreground=textColor, borderwidth=borderSize)
backToEntriesButton.grid(row=9,column=0, columnspan=2, sticky= "nsew")

#create the checkboxes for enableing digits, punctuations and letters small and big
checkboxForDigits = tk.Checkbutton(root, text="Use digits", command=UseDigits, variable=usedigits)
checkboxForDigits.grid(row=5,column=0, sticky= "nsew")

checkboxForPunctuations = tk.Checkbutton(root, text="Use punctuations", command=UsePunctuations, variable=usePunctuations)
checkboxForPunctuations.grid(row=5,column=1, sticky= "nsew")

checkboxForUppercase = tk.Checkbutton(root, text="Use uppercased lettes", command=UseUpperCase, variable=useUppercase)
checkboxForUppercase.grid(row=6,column=0, sticky= "nsew")

checkboxForLowercase= tk.Checkbutton(root, text="Use lowercased lettes", command=UseLowerCase, variable=useLowercase)
checkboxForLowercase.grid(row=6,column=1, sticky= "nsew")

#create entries UI
entries = []

l = 0
while l <= len(savedNames) - 1:
    newLabel = tk.Button(root, text="Test", command= lambda x=l: OpenEntry(x), borderwidth=borderSize)
    entries.append(newLabel)
    l += 1

l = 0
for entrie in entries:
    entrie.config(text= savedNames[l])
    l += 1

entries.sort(key=lambda b: b.cget("text").lower())

#create Entryapge
entryText = tk.Label(root, wraplength=wrapLengthForEntryTemplate)
entryText.config(font=label_font)

createEntryUI = [slider, nameInput, usernameInput, label, generateButton, clipboardButton, saveButton, backToEntriesButton, checkboxForDigits, checkboxForPunctuations, checkboxForLowercase, checkboxForUppercase]
entriesUI = []
entryTemplate = [entryText]

for element in entries:
    entriesUI.append(element)

for element in createEntryUI:
    element.grid_remove()

#create plus button
createEntryButton = tk.Button(root, text="+", compound="center",command=OpenCreateMenu, width=5, height=3, background=uiColorCode)

sideSelectionButton = []

i = 0
while i <= howManySides - 1:
    btn = tk.Button(sideSelectionFrame, command=lambda x= i: OpenSide(x), text=i)
    sideSelectionButton.append(btn)
    i += 1

OpenEntriesView()

root.bind("<Configure>", resize)

root.mainloop()