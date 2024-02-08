from machineDetails import MENU, machineResources, machineMoney
from decimal import Decimal
import os


def calculate_money_in_machine():
    machineMoney["machine_money"] = (machineMoney["machine_pennies"] * 0.01) \
                                  + (machineMoney["machine_nickels"] * 0.05) \
                                  + (machineMoney["machine_dimes"] * 0.10)   \
                                  + (machineMoney["machine_quarters"] * 0.25)


def calculate_change(pennies, nickels, dimes, quarters, change):
    machineMoney["machine_pennies"] += pennies
    machineMoney["machine_nickels"] += nickels
    machineMoney["machine_dimes"] += dimes
    machineMoney["machine_quarters"] += quarters

    if change >= 0.25:
        quarters = change // 0.25
        change -= quarters * 0.25
        machineMoney["machine_quarters"] -= quarters
    if change >= 0.10:
        dimes = change // 0.10
        change -= dimes * 0.10
        machineMoney["machine_dimes"] -= dimes
    if change >= 0.05:
        nickels = change // 0.05
        change -= nickels * 0.05
        machineMoney["machine_nickels"] -= nickels
    change = float(Decimal(str(change)).quantize(Decimal('0.01')))
    if change >= 0.01:
        pennies = change // 0.01
        change -= pennies * 0.01
        machineMoney["machine_pennies"] -= pennies
    calculate_money_in_machine()


def refund_money(pennies, nickels, dimes, quarters, change):
    machineMoney["machine_pennies"] -= pennies
    machineMoney["machine_nickels"] -= nickels
    machineMoney["machine_dimes"] -= dimes
    machineMoney["machine_quarters"] -= quarters
    machineMoney["machine_money"] -= MENU[userChoice]["cost"]

    if change >= 0.25:
        quarters = change // 0.25
        change -= quarters * 0.25
        machineMoney["machine_quarters"] += quarters
    if change >= 0.10:
        dimes = change // 0.10
        change -= dimes * 0.10
        machineMoney["machine_dimes"] += dimes
    if change >= 0.05:
        nickels = change // 0.05
        change -= nickels * 0.05
        machineMoney["machine_nickels"] += nickels
    change = float(Decimal(str(change)).quantize(Decimal('0.01')))
    if change >= 0.01:
        pennies = change // 0.01
        change -= pennies * 0.01
        machineMoney["machine_pennies"] += pennies
    calculate_money_in_machine()

    print("Your money were refunded!")


def check_for_resources_and_money():
    coffee = userChoice
    pennies = int(input("How many pennies: "))
    nickels = int(input("How many nickels: "))
    dimes = int(input("How many dimes: "))
    quarters = int(input("How many quarters: "))
    user_money = (pennies * 0.01) + (nickels * 0.05) + (dimes * 0.10) + (quarters * 0.25)
    if user_money >= MENU[userChoice]["cost"]:
        change = round(user_money - MENU[userChoice]["cost"], 2)
        calculate_change(pennies, nickels, dimes, quarters, change)
    else:
        print("You don't have enough")
        print("Your money were refunded!")
        return False

    if machineResources["machine_water"] >= MENU[userChoice]["water"]:
        # print("Water: Ok")
        machineResources["machine_water"] -= MENU[userChoice]["water"]
    else:
        print("Sorry not enough water")
        refund_money(pennies, nickels, dimes, quarters, change)
        input("Press Enter to continue")
        os.system('cls')
        return False
    if userChoice != "espresso":
        if machineResources["machine_milk"] >= MENU[userChoice]["milk"]:
            # print("Milk: Ok")
            machineResources["machine_milk"] -= MENU[userChoice]["milk"]
        else:
            print("Sorry not enough milk")
            refund_money(pennies, nickels, dimes, quarters, change)
            input("Press Enter to continue")
            os.system('cls')
            return False
    if machineResources["machine_coffee"] >= MENU[userChoice]["coffee"]:
        # print("Coffee: Ok")
        machineResources["machine_coffee"] -= MENU[userChoice]["coffee"]
        print(f"Your change is: {round(change, 2)}")
        print(f"Take your {coffee}!")
    else:
        print("Sorry not enough coffee")
        refund_money(pennies, nickels, dimes, quarters, change)
        input("Press Enter to continue")
        os.system('cls')
        return False

    return True


def refill_machine_resources():
    water = int(input("How many milliliters of water do you want to add: "))
    milk = int(input("How many milliliters of milk do you want to add: "))
    coffee = int(input("How many grams of coffee do you want to add: "))
    machineResources["machine_water"] += water
    machineResources["machine_milk"] += milk
    machineResources["machine_coffee"] += coffee
    print(f"You added {water} milliliters of water")
    print(f"You added {milk} milliliters of milk")
    print(f"You added {coffee} grams of coffee to the machine")


def refill_machine_money():
    pennies = int(input("How many pennies do you want to add: "))
    nickels = int(input("How many nickels do you want to add: "))
    dimes = int(input("How many dimes do you want to add: "))
    quarters = int(input("How many quarters do you want to add: "))
    machineMoney["machine_pennies"] += pennies
    machineMoney["machine_nickels"] += nickels
    machineMoney["machine_dimes"] += dimes
    machineMoney["machine_quarters"] += quarters
    print(f"You added {pennies} pennies to the machine")
    print(f"You added {nickels} nickels to the machine")
    print(f"You added {dimes} dimes to the machine")
    print(f"You added {quarters} quarters to the machine")
    calculate_money_in_machine()


def report_machine_resources():
    print(f"Machine water is: {machineResources['machine_water']} milliliters")
    print(f"Machine milk is: {machineResources['machine_milk']} milliliters")
    print(f"Machine coffee is: {machineResources['machine_coffee']} grams")


def report_machine_money():
    calculate_money_in_machine()
    print(f"Machine have: {machineMoney['machine_pennies']} pennies")
    print(f"Machine have: {machineMoney['machine_nickels']} nickels")
    print(f"Machine have: {machineMoney['machine_dimes']} dimes")
    print(f"Machine have: {machineMoney['machine_quarters']} quarters")
    print(f"Machine have: {machineMoney['machine_money']} money in total")


while True:
    userChoice = input("What do you want: espresso/latte/cappuccino ?: ").lower()
    if userChoice == "off":
        print("The machine is off!")
        input("Press Enter to continue")
        exit()
    if userChoice == "report":
        report_machine_resources()
        report_machine_money()
        input("Press Enter to continue")
        os.system('cls')
        continue
    if userChoice == "refill_r":
        refill_machine_resources()
        input("Press Enter to continue")
        os.system('cls')
        continue
    if userChoice == "refill_m":
        refill_machine_money()
        input("Press Enter to continue")
        os.system('cls')
        continue
    if userChoice == "espresso" or userChoice == "latte" or userChoice == "cappuccino":
        while check_for_resources_and_money():
            input("Press Enter to continue")
            os.system('cls')
            break
    else:
        print("Invalid Input")
        input("Press Enter to continue")
        os.system('cls')
        continue
