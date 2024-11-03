import os

import discord
from discord import app_commands

monkey = discord.Client(intents=discord.Intents.all())

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        monkey.load_extension(f"cogs.{filename[:-3]}")

@monkey.event
async def on_ready():
    print("ooga booga")

monkey.run(os.environ["token"])