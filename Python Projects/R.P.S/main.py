import os
import images
import random

images = [images.rock, images.paper, images.scissors]
userInput = ""

while userInput != 2:
    # print("0 = ROCK, 1 = PAPER, 2 = SCISSORS")
    print("If you want to play press (1) if you want to exit press (2)")
    userInput = int(input())
    if userInput == 2:
        exit()
    if userInput < 1 or userInput > 2:
        print("Invalid input")
        input("Press Enter to exit")
        exit()
    pc = random.randint(0, 2)

    print("Player: ")
    print(images[userInput])
    print("PC: ")
    print(images[pc])
    print("You: ")

    if userInput == 0:
        if pc == 0:
            print("Draw")
        elif pc == 1:
            print("Lose")
        else:
            print("Win")
    elif userInput == 1:
        if pc == 0:
            print("Win")
        elif pc == 1:
            print("Draw")
        else:
            print("Lose")
    else:
        if pc == 0:
            print("Lose")
        elif pc == 1:
            print("Win")
        else:
            print("Draw")

    userInput = input("Press Enter to continue")
    os.system('cls')