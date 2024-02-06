import os
import random

randNum = 0
guessNum = 0
attempts = 0
isItWin = True
uInput = ""

while True:
    randNum = random.randint(0, 100)
    print(randNum)
    print("Welcome to my GuessGame!")
    print("If you want to play please choose game mode: easy/hard")
    print("If you want to exit press 'e'")
    uInput = input(": ").lower()
    if uInput == "e":
        exit()
    elif uInput == "easy":
        attempts = 10
        print("The number is between 1-100")
    elif uInput == "hard":
        attempts = 5
        print("The number is between 1-100")
    else:
        print("Wrong Input!")
        exit()
    while attempts > 0:
        print(f"You have {attempts} left")
        guessNum = int(input("Enter your guess: "))

        if guessNum < 1 or guessNum > 100:
            print("The number is between 1-100!!!")
            attempts -= 1
        elif guessNum == randNum:
            print("Right in the spot!")
            break
        elif guessNum > randNum:
            print("Too high")
            attempts -= 1
        elif guessNum < randNum:
            print("Too low")
            attempts -= 1
        else:
            print("Error")
            break
    if attempts > 0:
        print("You WON!")
    else:
        print("You LOST!")
    uInput = input("Press Enter to continue: ")
    os.system('cls')