import random

from discord.ext import commands

class Handlers(commands.Cog):
    def __init__(self, bot, db):
        self.monkey = bot
        self.db = db

    # @commands.Cog.listener("on_message")
    # async def on_message(self, message):
        # if message.author.bot:
            # return

        # await self.on_message_money(message)
        # await self.on_message_spawn(message)

    @commands.Cog.listener("on_message")
    async def on_message_money(self, message):
        if len(message.content) >= 3:    
            if not self.db.is_user(message.author.id):
                self.db.new_user(message.author.id)
            else:
                self.db.add_money(message.author.id, random.randint(5, 15))

    @commands.Cog.listener("on_message")
    async def on_message_spawn(self, message):
        if len(message.content) >= 3:
            c_id = str(message.channel.id)
            
            if c_id not in self.db.cache:
                self.db.cache["chanels"][c_id] = 0
            else:
                self.db.cache["chanels"][c_id] += 1

            spawn = random.randint(1, 400)    
            if spawn <= self.db.cache["chanels"][c_id]:
                self.db.cache["chanels"][c_id] = 0
                await message.channel.send("monkey spawn here")

async def setup(bot, db):
    await bot.add_cog(Handlers(bot, db))