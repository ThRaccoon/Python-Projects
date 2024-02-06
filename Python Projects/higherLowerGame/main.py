from informationSheet import listOfInfo
import random
import os

correctGuess = False
playerGuess = False
randNumList = []
breaker = True
counter = 0


def drawInfo(listOfInfo):
    randNumList.clear()
    randNum1 = random.randint(0, len(listOfInfo) - 1)
    randNum2 = random.randint(0, len(listOfInfo) - 1)
    if randNum1 == randNum2:
        while randNum1 == randNum2:
            randNum1 = random.randint(0, len(listOfInfo) - 1)
        print(f"Name: {listOfInfo[randNum1]['Name']}")
        print(f"Info: {listOfInfo[randNum1]['Info']}")
        print()
        print(f"Name: {listOfInfo[randNum2]['Name']}")
        print(f"Info: {listOfInfo[randNum2]['Info']}")
        print()
    else:
        print(f"Name: {listOfInfo[randNum1]['Name']}")
        print(f"Info: {listOfInfo[randNum1]['Info']}")
        print()
        print(f"Name: {listOfInfo[randNum2]['Name']}")
        print(f"Info: {listOfInfo[randNum2]['Info']}")
        print()

    randNumList.append(randNum1)
    randNumList.append(randNum2)
    return randNumList


def chooseCorrectGuess(randNumList, correctGuess):
    randNum1 = randNumList[0]
    randNum2 = randNumList[1]
    if listOfInfo[randNum1]["Score"] \
            > listOfInfo[randNum2]["Score"]:
        print("Debug: A")
        correctGuess = True

    else:
        print("Debug: B")
        correctGuess = False

    return correctGuess


while breaker:
    os.system('cls')
    drawInfo(listOfInfo)
    correctGuess = chooseCorrectGuess(randNumList, correctGuess)

    uInput = ""
    print(f"Your score is: {counter}")
    uInput = input("Which is bigger A or B?: ").lower()

    if uInput == "a":
        playerGuess = True
    else:
        playerGuess = False

    if playerGuess == correctGuess:
        counter += 1
    else:
        print("WRONG! YOU LOST!")
        print(f"Your score is: {counter}")
        breaker = False
        uInput = input("Press Enter to continue")
