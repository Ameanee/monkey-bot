import random

import discord
from discord import app_commands
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot, db):
        self.monkey = bot
        self.db = db

    @app_commands.command(name="balance", description="\"My pants your house rent\" -Polo G")
    async def balance(self, interaction: discord.Interaction, user: discord.User = None):
        if user is None:
            user = interaction.user

        if not self.db.is_user(user.id):
            self.db.new_user(user.id)

        embed = discord.Embed(title=f"{user.display_name}'s balance", color=0x00ff00)
        embed.add_field(name="Money", value=f"{self.db.balance(user.id)}")
        
        await interaction.response.send_message(f"{user.mention}", embed=embed)

    @app_commands.command(name="give", description="free robux giveaway!!!")
    async def give(self, interaction: discord.Interaction, user: discord.User, amount: int):
        if not self.db.is_user(interaction.user.id):
            self.db.new_user(interaction.user.id)

        if not self.db.is_user(user.id):
            self.db.new_user(user.id)

        if self.db.balance(interaction.user.id) < amount:
            await interaction.response.send_message(f"@everyone {user.mention} is a brokie")
            return

        self.db.add_money(interaction.user.id, -amount)
        self.db.add_money(user.id, amount)

        await interaction.response.send_message(":thumbs_up:")

async def setup(bot, db):
    await bot.add_cog(Economy(bot, db))