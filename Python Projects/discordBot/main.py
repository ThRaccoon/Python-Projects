import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import datetime

BOT = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@BOT.event
async def on_ready():
    print("Ready")


@BOT.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(f"{ctx.author.mention} This command is not found!")


# List of ban members---------------------------------------------------------------------------------------------------
@BOT.command()
@has_permissions(administrator=True)
async def rban_list(ctx):
    list_of_bans = []
    async for ban in ctx.guild.bans():
        _name = str(ban.user)
        _reason = str(ban.reason)
        name_and_reason = _name + ": " + _reason
        list_of_bans.append(name_and_reason)
    if len(list_of_bans) == 0:
        await ctx.send(f"{ctx.author.mention} ban list is empty!")
    else:
        for i in list_of_bans:
            await ctx.send(i)


# Check for errors
@rban_list.error
async def rban_list_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} You don't have the permission to do this!")


# Kick command----------------------------------------------------------------------------------------------------------
@BOT.command()
@has_permissions(administrator=True)
async def rkick(ctx, member: discord.Member, *, reason: str):
    await member.kick(reason=reason)
    await ctx.send(f"{ctx.author.mention} kicked {member.global_name}({member.name}) - reason: {reason}")
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = f"{ctx.author.global_name} kicked {member.global_name}({member.name}) - reason: {reason} on {time_now}"
    with open("kick_data.txt", "a") as kick_file:
        kick_file.write(data + '\n')


# Check for errors
@rkick.error
async def rkick_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Member not found!")
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Please add a reason!")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} You don't have the permission to do this!")
# ----------------------------------------------------------------------------------------------------------------------


# Ban command-----------------------------------------------------------------------------------------------------------
@BOT.command()
@has_permissions(administrator=True)
async def rban(ctx, member: discord.Member, *, reason: str):
    await member.ban(reason=reason)
    await ctx.send(f"{ctx.author.mention} banned {member.global_name}({member.name}) - reason: {reason}")
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = f"{ctx.author.global_name} banned {member.global_name}({member.name}) - reason: {reason} on {time_now}"
    with open("ban_data.txt", "a") as ban_file:
        ban_file.write(data + '\n')


# Check for errors
@rban.error
async def rban_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Member not found!")
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Please add a reason!")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} You don't have the permission to do this!")
# ----------------------------------------------------------------------------------------------------------------------


# Roll with custom bounds-----------------------------------------------------------------------------------------------
@BOT.command()
async def rroll(ctx, num1: int, num2: int):
    if 0 < num1 < 1001 and 0 < num2 < 1001:
        await ctx.send(f"{ctx.author.mention} rolled {random.randint(num1, num2)}")
    else:
        await ctx.send(f"{ctx.author.mention} Use only numbers between 1 and 1000!")


# Roll from 1 to 100----------------------------------------------------------------------------------------------------
@BOT.command()
async def rroll100(ctx):
    await ctx.send(f"{ctx.author.mention} rolled {random.randint(1, 100)}")


# Check for errors
@rroll.error
async def rroll_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} You need to put lower bound and upper bound for the roll! "
                       f"Ex: !rroll 1 10")
# ----------------------------------------------------------------------------------------------------------------------


# Help command----------------------------------------------------------------------------------------------------------
@BOT.command()
async def rhelp(ctx):
    with open("help.txt", "r") as help_file:
        text = help_file.read()
    await ctx.send(text)
# ----------------------------------------------------------------------------------------------------------------------


# Token-----------------------------------------------------------------------------------------------------------------
with open("token.txt") as token_file:
    token = token_file.read()
BOT.run(token)
# ----------------------------------------------------------------------------------------------------------------------
