import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import re

BOT = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@BOT.event
async def on_ready():
    print("Ready")


@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("This command is not found!")


@BOT.command()
async def relo(ctx, steam_id: str):

    site_url = "https://faceitanalyser.com/stats/"

    pattern = r'>([^<]+)<'
    _list = ["cs2", "csgo"]

    if len(steam_id) > 30:
        if "id" in steam_id:
            steam_id = steam_id[30:]
        else:
            steam_id = steam_id[36:]
    else:
        await ctx.send(f"{ctx.author.mention} this steam id is too short!")
        return

    if steam_id[-1] == '/':
        steam_id = steam_id[:len(steam_id) - 1]

    for i in range(len(_list)):
        request = requests.get(url=f"{site_url}{steam_id}/{_list[i]}")
        soup = BeautifulSoup(request.content, features="html.parser")

        if soup.find(string="Player Not Found"):
            await ctx.send("Player not found!")
            if soup.find(string="Did you mean:"):
                await ctx.send("Did you mean:")
                spans = soup.find_all('span', class_=True)
                spans = str(spans)
                matches = re.findall(pattern, spans)
                await ctx.send(''.join(matches))
                return
            else:
                return
        try:
            name = soup.find('span', class_="stats_profile_name_span").text.strip()
            elo = soup.find("span", class_="stats_profile_elo_span").text.strip()
            avg_kdr = soup.find(string="Avg. KDR").find_next().text.strip()
            hltv = soup.find(string="HLTV").find_next().text.strip()
            winrate = soup.find(string="Winrate").find_next().text.strip()
            await ctx.send(f"{_list[i].upper()}\n"
                           f"{name}\n"
                           f"{elo}\n"
                           f"{avg_kdr} Avg. KDR\n"
                           f"{hltv} HLTV rating\n"
                           f"{winrate}% Winrate")
        except AttributeError:
            await ctx.send(f"No matches played on {_list[i].upper()}")


@relo.error
async def relo_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} Please enter steam profile URL!")

# Token-----------------------------------------------------------------------------------------------------------------
with open("token.txt") as file:
    token = file.read()
BOT.run(token)
# ----------------------------------------------------------------------------------------------------------------------
