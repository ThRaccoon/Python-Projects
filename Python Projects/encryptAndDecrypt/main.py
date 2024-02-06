from encrypt import encrypt
from decrypt import decrypt

eStr = ""
dStr = ""
userInput = ""

while True:
    mode = input("Mode Encrypt or Decrypt: ").lower()
    text = input("Enter text: ")
    key = int(input("Enter key [should be a number!]: "))
    if mode == "encrypt" or mode == "e":
        eStr = encrypt(text, key)
        print("The encrypted text is " + eStr)
    elif mode == "decrypt" or mode == "d":
        dStr = decrypt(text, key)
        print("The decrypted text is " + dStr)
    else:
        print("(Error): Wrong mode!")
        userInput = input("Press Enter to try again")

    userInput = input("To use again press: [1] \nTo exit press:      [2] ").lower()
    if userInput == "2":
        break
