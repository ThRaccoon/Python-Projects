from art import drawStickMan
import random
import os

listOfWords = ["dog", "cat", "raccoon", "bear", "frog"]
randNum = random.randint(0, len(listOfWords) - 1)
chosenWord = listOfWords[randNum]
displayWord = []
attempts = 6
counter = 0
userInput = ""

for x in range(0, len(chosenWord)):
    displayWord.append("_")


while True:
    os.system('cls')
    print("Word: " + ''.join(displayWord))
    print(f"You have {attempts} attempt/s left!")
    print(drawStickMan(attempts))
    guessLetter = input("Your letter is: ").lower()
    for y in range(0, len(chosenWord)):
        if guessLetter == chosenWord[y]:
            displayWord[y] = guessLetter
            print("Word: " + ''.join(displayWord))
            print(f"You have {attempts} attempt/s left!")
            print(drawStickMan(attempts))
            counter += 1
    if counter == 0:
        attempts -= 1
        print("Word: " + ''.join(displayWord))
        print(f"You have {attempts} attempt/s left!")
        print(drawStickMan(attempts))

        if attempts == 0:
            os.system('cls')
            print("You Lost!")
            print(drawStickMan(attempts))
            userInput = input("Press Enter to continue")
            break
    else:
        if "_" not in displayWord:
            os.system('cls')
            print("You Won!")
            print("The word is: " + ''.join(displayWord))
            print(f"You have {attempts} attempt/s left!")
            print(drawStickMan(attempts))
            userInput = input("Press Enter to continue")
            break
    counter = 0
