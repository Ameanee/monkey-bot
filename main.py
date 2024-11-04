import os

from db import db

import discord
from discord.ext import commands

import cogs.handlers, cogs.economy

db = db()
monkey = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@monkey.event
async def on_ready():
    await cogs.handlers.setup(monkey, db)
    await cogs.economy.setup(monkey, db)

    await monkey.tree.sync()

    print("ooga booga")

monkey.run(os.environ["token"])