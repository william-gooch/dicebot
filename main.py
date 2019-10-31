import discord
from discord.ext import commands
import re
from dice_parser import Interpreter

dicebot = commands.Bot(command_prefix="!")


def roll(arg):
    result = Interpreter(arg).interpret()
    message = "```" + '\n'.join(
        [f"{', '.join(map(str, r[0]))} + {r[2]}: {r[3]} (drop {', '.join(map(str, r[1]))})" for r in result]) + "```"
    return message


@dicebot.command(name="r")
async def dicebot_roll(ctx, arg):
    await ctx.send(roll(arg))


@dicebot.command(name="char")
async def dicebot_char(ctx):
    await ctx.send(roll("4d6xl1r6"))


@dicebot.event
async def on_ready():
    print(f"Logged in as {dicebot.user}")

dicebot.run('NjA3OTAxODA4OTY2NTAwMzYz.XUgXAQ.JQNiMA6MRhHxvg58HODaYUvQ-rQ')
