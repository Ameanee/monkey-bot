import random

import discord
from discord.ext import commands

class spawnViews(discord.ui.View):
    def __init__(self, db, type: str, monkeys):
        super().__init__()
        self.monkeys = monkeys
        self.db = db
        self.type = type
        self.caught = False

    @discord.ui.button(label="Catch", style=discord.ButtonStyle.green)
    async def catch(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.caught:
            self.caught = True
            button.disabled = True

            id = self.monkeys.new_monkey(self.type, interaction.guild.name)
            self.db.add_monkey(interaction.user.id, id)

            await interaction.message.edit(view=self)
            await interaction.response.send_message(f"{interaction.user.mention} caught it!")

class Handlers(commands.Cog):
    def __init__(self, bot, db, monkeys):
        self.monkeys = monkeys
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
        if len(message.content) >= 3 and message.author.id != self.monkey.user.id:    
            if not self.db.is_user(message.author.id):
                self.db.new_user(message.author.id)
            else:
                self.db.add_money(message.author.id, random.randint(5, 15))

    @commands.Cog.listener("on_message")
    async def on_message_spawn(self, message):
        if len(message.content) >= 3 and message.author.id != self.monkey.user.id:
            c_id = str(message.channel.id)
            
            if c_id not in self.db.cache["chanels"]:
                self.db.cache["chanels"][c_id] = 0
            else:
                self.db.cache["chanels"][c_id] += 1

            spawn = random.randint(1, 2)    
            if spawn <= self.db.cache["chanels"][c_id]:
                self.db.cache["chanels"][c_id] = 0
                m_type = self.monkeys.random_monkey()
                await message.channel.send(f"monkey spawn here {m_type}", view=spawnViews(self.db, m_type, self.monkeys))

async def setup(bot, db, monkeys):
    await bot.add_cog(Handlers(bot, db, monkeys))