def addition(num1, num2):
    return num1 + num2


def subtraction(num1, num2):
    return num1 - num2


def multiplication(num1, num2):
    return num1 * num2


def division(num1, num2):
    return num1 / num2


listOfOperators = {
    "+": addition,
    "-": subtraction,
    "*": multiplication,
    "/": division,
}

func = ""
num1 = 0.
op = ""
num2 = 0.
result = 0.
userInput = ""

while True:
    num1 = float(input("Enter first number: "))
    while True:
        op = input("Enter operator: ")
        num2 = float(input("Enter second number: "))
        func = listOfOperators[op]
        result = func(num1, num2)
        print(result)
        userInput = input(
            f"Do you want to continue calculating with {result}? y/n: ").lower()
        if userInput == "y":
            num1 = result
        else:
            userInput = input("Press E for exit or press N for new calculation: ").lower()
            if userInput == "n":
                break
            else:
                exit()
