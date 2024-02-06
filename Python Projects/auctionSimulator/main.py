import os


def findTheHighestBider(listOfBiders):
    mbid = 0
    winner = ""
    for x in listOfBiders:
        if mbid < listOfBiders[x]:
            mbid = listOfBiders[x]
            winner = x
    result = [winner, mbid]
    return result


listOfBiders = {}
name = ""
bid = 0
userInput = ""

while True:
    name = input("What is your name: ")
    bid = int(input("How much will you bid: $"))
    listOfBiders[name] = bid
    userInput = input("Do you want to continue? yes/no: ").lower()
    if userInput == "yes":
        os.system('cls')
    elif userInput == "no":
        os.system('cls')
        break
    else:
        print("Invalid input!")
        input("Press Enter to exit")
        exit()

result = findTheHighestBider(listOfBiders)
print(f"The winner is {result[0]} with bid of {result[1]}$ !")
input("Press Enter to exit")
