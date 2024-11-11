import os

from db import db

import discord
from discord.ext import commands

import cogs.handlers, cogs.economy
import models.monkeys

db = db()
monkey = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@monkey.event
async def on_ready():
    await cogs.handlers.setup(monkey, db, models.monkeys.Monkeys(db))
    await cogs.economy.setup(monkey, db, models.monkeys.Monkeys(db))

    await monkey.tree.sync()

    print("ooga booga")

monkey.run(os.environ["token"])