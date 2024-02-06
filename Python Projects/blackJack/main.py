from deck import cardDeck
import random
import os


def drawCard(Deck, deckSum):
    newCard = 0
    newCard = random.randint(0, len(cardDeck) - 1)
    if cardDeck[newCard] == 11:
        if deckSum <= 10:
            Deck.append(11)
            return Deck
        else:
            Deck.append(1)
            return Deck
    Deck.append(cardDeck[newCard])
    return Deck


def sumCards(Deck):
    sum = 0
    for x in range(0, len(Deck)):
        sum += Deck[x]
    return sum


def checkForBJ(pDeckSum, dDeckSum):
    if pDeckSum == dDeckSum and pDeckSum == 21:
        print("DRAW! BOTH SIDES HAVE BLACK JACK!")
        return False
    elif pDeckSum == 21:
        print("Player WON WITH BLACK JACK!")
        return False
    elif dDeckSum == 21:
        print("Dealer WON WITH BLACK JACK!")
        return False
    else:
        return True


def checkWhoWon(pDeckSum, dDeckSum):
    if pDeckSum == dDeckSum:
        print("Draw")
    elif pDeckSum > 21 and dDeckSum > 21:
        print("BOTH SIDES LOSS")
    elif dDeckSum > 21 or (pDeckSum > dDeckSum and pDeckSum <= 21):
        print("Player WON")
    elif pDeckSum > 21 or (dDeckSum > pDeckSum and dDeckSum <= 21):
        print("Dealer WON")
    else:
        print("ERROR")


def printPlayerInfo(pDeck, pDeckSum, dDeck):
    print(f"Your hand is: {pDeck} and the sum is: {pDeckSum}")
    print(f"Dealer first card is {dDeck[0]}")


pDeck = []
pDeckSum = 0
dDeck = []
dDeckSum = 0

uInput = ""
isItBJ = True
isItlose = True

while True:
    os.system('cls')
    uInput = input("Do you want to play a game of BLACKJACK? y/n: ")
    if uInput == "n":
        exit()
    elif uInput == "y":
        uInput = ""
        for x in range(0, 2):
            pDeck = drawCard(pDeck, pDeckSum)
            pDeckSum = sumCards(pDeck)
            dDeck = drawCard(dDeck, dDeckSum)
            dDeckSum = sumCards(dDeck)

        printPlayerInfo(pDeck, pDeckSum, dDeck)
        isItBJ = checkForBJ(pDeckSum, dDeckSum)
        while pDeckSum < 21:
            uInput = input("Do you want to pull another card? (y/n): ").lower()
            if uInput == "y":
                pDeck = drawCard(pDeck, pDeckSum)
                pDeckSum = sumCards(pDeck)
                isItBJ = checkForBJ(pDeckSum, dDeckSum)
                printPlayerInfo(pDeck, pDeckSum, dDeck)
            else:
                while dDeckSum < 14:
                    dDeck = drawCard(dDeck, dDeckSum)
                    dDeckSum = sumCards(dDeck)
                isItBJ = checkForBJ(pDeckSum, dDeckSum)
                break
    else:
        print("Invalid Input!")
        uInput = input("Press Enter to continue")
        break

    checkWhoWon(pDeckSum, dDeckSum)
    print(f"Player deck is: {pDeck} and the sum is: {pDeckSum}")
    print(f"Dealer deck is: {dDeck} and the sum is: {dDeckSum}")
    uInput = input("Press Enter to continue: ")

    pDeck.clear()
    pDeckSum = 0
    dDeck.clear()
    dDeckSum = 0
