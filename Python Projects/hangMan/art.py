def drawStickMan(attempts):
    print("--|")
    if attempts <= 5:
        print("  0")
    if attempts == 4:
        print(" /")
    elif attempts == 3:
        print(" /|")
    elif attempts <= 2:
        print(" /|\\")
    if attempts == 1:
        print(" /")
    elif attempts == 0:
        print(" / \\")
    print("")

    return " "
