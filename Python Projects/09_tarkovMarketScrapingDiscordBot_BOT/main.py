import discord
from discord.ext import commands
import selenium
from selenium import webdriver
import selenium.common.exceptions
from bs4 import BeautifulSoup
import time


BOT = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# ----------------------------------------------------------------------------------------------------------------------
driver = webdriver.Firefox()
traders_list = ["Fence", "Jaeger", "Lightkeeper", "Mechanic", "Peacekeeper", "Prapor", "Ragman", "Skier", "Therapist"]
URL_1 = "https://tarkov-market.com/item/pm_fab_defense_pistol_grip"
URL_2 = "https://tarkov.app/track/items?i=a:3"
# ----------------------------------------------------------------------------------------------------------------------


@BOT.event
async def on_ready():
    print("Ready")


@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("This command is not found!")


# Check all the result of the string that you entered-------------------------------------------------------------------
@BOT.command()
async def res_list(ctx, *, item_name: str):
    embed = discord.Embed(
        title=item_name,
        color=discord.Color.darker_gray(),
    )

    try:
        driver.get(URL_1)
    except selenium.common.exceptions.NoSuchElementException:
        ctx.send("URL for Tarkov Market can't be found (Error 404)")

    item_list = []

    try:
        crawler = driver.find_element("xpath", '//input[@placeholder="Search"]')
        for i in range(len(item_name)):
            if i == len(item_name) - 1:
                time.sleep(1)
                crawler.send_keys(item_name[i])
            else:
                crawler.send_keys(item_name[i])
                time.sleep(0.01)
    except selenium.common.exceptions.NoSuchElementException:
        ctx.send("Error: Selenium can't find the search bar!")

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    data = soup.find_all('img', alt=True)

    alt_texts = [img['alt'] for img in data]
    for alt in alt_texts:
        item_list.append(alt)

    alt_texts = '\n'.join(item_list)
    embed.add_field(name="Search result:", value=alt_texts)

    await ctx.send(embed=embed)


@res_list.error
async def ser_list_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Please enter item name!")


# Check if item is needed for quests------------------------------------------------------------------------------------
@BOT.command()
async def q_ch(ctx, *, item_name: str):

    try:
        driver.get(URL_2)
    except selenium.common.exceptions.NoSuchElementException:
        ctx.send("(Error 404) URL for Tarkov.app is not found!")

    quests = ""

    # Checks if the item is needed for any quests
    try:
        crawler = driver.find_element("xpath", '//input[@placeholder="Search"]')
        crawler.send_keys(str(item_name))
    except selenium.common.exceptions.NoSuchElementException:
        ctx.send("Error: Selenium can't find the search bar!")

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        quests = soup.find('div', class_="sc-fLcnxK fHnjCl").text.replace("0", "").replace("/", "")
        is_needed_for_quests = True
        name = soup.find('div', class_="sc-lllmON dihqVX").text
    except AttributeError:
        is_needed_for_quests = False
        name = item_name

    embed = discord.Embed(
        title=name,
        color=discord.Color.darker_gray(),
    )

    if is_needed_for_quests:
        embed.add_field(name="is needed for quests:", value=quests)
    else:
        embed.add_field(name="is needed for quests:", value="None")

    await ctx.send(embed=embed)


@q_ch.error
async def q_ch_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Please enter item name!")


# Full search-----------------------------------------------------------------------------------------------------------
@BOT.command()
async def f_ser(ctx, *, item_name: str):
    embed = discord.Embed(
        title=item_name,
        color=discord.Color.darker_gray(),
    )

    try:
        driver.get(URL_1)
    except selenium.common.exceptions.NoSuchElementException:
        ctx.send("(Error 404) URL for Tarkov Market is not found!")

    slots = ""
    trader = ""
    quests = ""
    temp_list = []

    try:
        crawler = driver.find_element("xpath", '//input[@placeholder="Search"]')
        for i in range(len(item_name)):
            if i == len(item_name) - 1:
                time.sleep(1)
                crawler.send_keys(item_name[i])
            else:
                crawler.send_keys(item_name[i])
                time.sleep(0.01)
    except selenium.common.exceptions.NoSuchElementException:
        ctx.send("Error: Selenium can't find the search bar!")

    time.sleep(2)

    try:
        crawler = driver.find_element("xpath", '//a[@class="suggest-item"]')
        crawler.click()
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Item name
        name = soup.find('h1', class_="title")
        name = name.findChild('span').contents[0]

        # Item price
        price = soup.find('div', class_="big bold alt").text
        currency = price[-1]
        price = price.replace(",", "").replace(currency, "")

        # Price per slot
        for j in soup.find_all('div', class_="small"):
            temp_list.append(j.text)
        slots_word = temp_list[2]

        for i in range(len(slots_word)):
            if slots_word[i].isdigit():
                slots += slots_word[i]
        price_per_slot = int(price) / int(slots)

        # Checks if it can be sold at the flea market
        try:
            driver.find_element("xpath", '//div[@class="my-15 minus"]').is_displayed()
            flea_marketable = False
        except selenium.common.exceptions.NoSuchElementException:
            flea_marketable = True

        # Best trader to sell
        trader_to_sell = soup.find('div', string="Sell to trader")
        trader_to_sell = trader_to_sell.parent
        trader_to_sell.findChild('div', {'class': False})
        trader_to_sell = trader_to_sell.text

        for i in range(len(traders_list)):
            if traders_list[i] in trader_to_sell:
                trader = traders_list[i]
                break

        try:
            driver.get(URL_2)
        except selenium.common.exceptions.NoSuchElementException:
            ctx.send("(Error 404) URL for Tarkov.app is not found!")

        # Checks if the item is needed for any quests
        try:
            crawler = driver.find_element("xpath", '//input[@placeholder="Search"]')
            crawler.send_keys(str(name))
        except selenium.common.exceptions.NoSuchElementException:
            ctx.send("Error: Selenium can't find the search bar!")

        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        try:
            quests = soup.find('div', class_="sc-fLcnxK fHnjCl").text.replace("0", "").replace("/", "")
            is_needed_for_quests = True
        except AttributeError:
            is_needed_for_quests = False

        if not flea_marketable:
            embed.title = f"Item name: {name}"
            embed.add_field(name="Banned from flea:", value="Yes")
            embed.add_field(name="Price:", value=f"{price}{currency}")
            embed.add_field(name="Price per slot:", value=f"{round(price_per_slot, 2)}{currency}")
            embed.add_field(name="Slots:", value=slots)
            embed.add_field(name="Best trader to sell:", value=trader)
        else:
            embed.title = f"Item name: {name}"
            embed.add_field(name="Banned from flea:", value="No")
            embed.add_field(name="Flea price:", value=f"{price}{currency}")
            embed.add_field(name="Price per slot:", value=f"{round(price_per_slot, 2)}{currency}")
            embed.add_field(name="Slots:", value=slots)
            embed.add_field(name="Best trader to sell:", value=trader)

        if is_needed_for_quests:
            embed.add_field(name="Needed for quests:", value=quests)
        else:
            embed.add_field(name="Needed for quests:", value="None")

        await ctx.send(embed=embed)

    except selenium.common.exceptions.NoSuchElementException:
        await ctx.send(f"{item_name} does not exist!")


@f_ser.error
async def f_ser_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Please enter item name!")


# Half search-----------------------------------------------------------------------------------------------------------
@BOT.command()
async def h_ser(ctx, *, item_name: str):
    embed = discord.Embed(
        title=item_name,
        color=discord.Color.darker_gray(),
    )

    try:
        driver.get(URL_1)
    except selenium.common.exceptions.NoSuchElementException:
        ctx.send("URL for Tarkov Market can't be found (Error 404)")

    slots = ""
    trader = ""
    temp_list = []

    try:
        crawler = driver.find_element("xpath", '//input[@placeholder="Search"]')
        for i in range(len(item_name)):
            if i == len(item_name) - 1:
                time.sleep(1)
                crawler.send_keys(item_name[i])
            else:
                crawler.send_keys(item_name[i])
                time.sleep(0.01)
    except selenium.common.exceptions.NoSuchElementException:
        ctx.send("Error: Selenium can't find the search bar!")

    time.sleep(2)

    try:
        crawler = driver.find_element("xpath", '//a[@class="suggest-item"]')
        crawler.click()

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Item name
        name = soup.find('h1', class_="title")
        name = name.findChild('span').contents[0]

        # Item price
        price = soup.find('div', class_="big bold alt").text
        currency = price[-1]
        price = price.replace(",", "").replace(currency, "")

        # Price per slot
        for j in soup.find_all('div', class_="small"):
            temp_list.append(j.text)
        slots_word = temp_list[2]

        for i in range(len(slots_word)):
            if slots_word[i].isdigit():
                slots += slots_word[i]
        price_per_slot = int(price) / int(slots)

        # Checks if it can be sold at the flea market
        try:
            driver.find_element("xpath", '//div[@class="my-15 minus"]').is_displayed()
            flea_marketable = False
        except selenium.common.exceptions.NoSuchElementException:
            flea_marketable = True

        # Best trader to sell
        trader_to_sell = soup.find('div', string="Sell to trader")
        trader_to_sell = trader_to_sell.parent
        trader_to_sell.findChild('div', {'class': False})
        trader_to_sell = trader_to_sell.text

        for i in range(len(traders_list)):
            if traders_list[i] in trader_to_sell:
                trader = traders_list[i]
                break

        if not flea_marketable:
            embed.title = f"Item name: {name}"
            embed.add_field(name="Banned from flea:", value="Yes")
            embed.add_field(name="Price:", value=f"{price}{currency}")
            embed.add_field(name="Price per slot:", value=f"{round(price_per_slot, 2)}{currency}")
            embed.add_field(name="Slots:", value=slots)
            embed.add_field(name="Best trader to sell:", value=trader)
        else:
            embed.title = f"Item name: {name}"
            embed.add_field(name="Banned from flea:", value="No")
            embed.add_field(name="Flea price:", value=f"{price}{currency}")
            embed.add_field(name="Price per slot:", value=f"{round(price_per_slot, 2)}{currency}")
            embed.add_field(name="Slots:", value=slots)
            embed.add_field(name="Best trader to sell:", value=trader)

        await ctx.send(embed=embed)

    except selenium.common.exceptions.NoSuchElementException:
        await ctx.send(f"{item_name} does not exist!")


@h_ser.error
async def h_ser_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Please enter item name!")


# Help command----------------------------------------------------------------------------------------------------------
@BOT.command()
async def rhelp(ctx):

    with open("help.txt", "r") as help_file:
        data = help_file.read()
    await ctx.send(data)

# Token-----------------------------------------------------------------------------------------------------------------
with open("token.txt") as file:
    token = file.read()
BOT.run(token)
# ----------------------------------------------------------------------------------------------------------------------
