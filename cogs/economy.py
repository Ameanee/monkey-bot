import discord
from discord import app_commands
from discord.ext import commands

class tradeViews (discord.ui.View):
    def __init__ (self, db, me, them, give_money, ask_money, give_monkeys, ask_monkeys, embed):
        super().__init__()
        self.db = db
        self.me = me
        self.them = them
        self.give_money = give_money
        self.ask_money = ask_money
        self.give_monkeys = give_monkeys
        self.ask_monkeys = ask_monkeys
        self.embed = embed
        self.done = False

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button): # must add exploit preventer later
        if not self.done and interaction.user.id == self.them.id:
            self.done = True
        
            self.db.add_money(self.me.id, self.ask_money - self.give_money)
            self.db.add_money(self.them.id, self.give_money - self.ask_money)
    
            for monkey in self.give_monkeys:
                self.db.add_monkey(self.them.id, monkey)
                self.db.remove_monkey(self.me.id, monkey)
    
            for monkey in self.ask_monkeys:
                self.db.add_monkey(self.me.id, monkey)
                self.db.remove_monkey(self.them.id, monkey)    

            self.embed.color = 0x00FF00
            await interaction.response.edit_message(embed=self.embed, view=None)
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.done and (interaction.user.id == self.them.id or interaction.user.id == self.me.id):
            self.done = True
            
            for item in self.children:
                item.disabled = True
    
            self.embed.color = 0xFF0000
            await interaction.message.edit(embed=self.embed, view=self)

class Economy(commands.Cog):
    def __init__(self, bot, db, monkeys, items):
        self.monkey = bot
        self.db = db
        self.monkeys = monkeys
        self.items = items

    lookup = app_commands.Group(name="lookup", description="hot girls near me!")
    sell = app_commands.Group(name="sell", description="sell your stuff!")

    @lookup.command(name="monkey", description="robloxtrading.com")
    async def lookup_monkey(self, interaction: discord.Interaction, id: str):
        monkey = self.db.get_monkey(id)

        if monkey is None:
            await interaction.response.send_message("your dad!")
            return
            
        embed = discord.Embed(title=f"{monkey[1]} `#{id}`")
        embed.add_field(name="Health", value=f"{monkey[2]}/{monkey[2]} :heart:")
        embed.add_field(name="Damage", value=f"{monkey[3]} :crossed_swords:")
        embed.add_field(name="Origin", value=f"<t:{monkey[6]}> in {monkey[5]}", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @sell.command(name="monkey", description="lincoln legacy")
    async def sell_monkey(self, interaction: discord.Interaction, id: int):
        if not self.db.is_user(interaction.user.id):
            self.db.new_user(interaction.user.id)

        if id not in self.db.get_monkeys(interaction.user.id):
            await interaction.response.send_message("your dad!")
            return

        type = self.monkeys.monkeys[self.db.get_monkey(id)[1]]["rarity"]
        self.db.remove_monkey(interaction.user.id, id, True)
        self.db.add_money(interaction.user.id, self.monkeys.prices[type])
        await interaction.response.send_message(f"sold for {self.monkeys.prices[type]}!")  

    @app_commands.command(name="balance", description="\"My pants your house rent\" -Polo G")
    async def balance(self, interaction: discord.Interaction, user: discord.User = None):
        if user is None:
            user = interaction.user

        if not self.db.is_user(user.id):
            self.db.new_user(user.id)

        embed = discord.Embed(title=f"{user.display_name}'s balance", color=0x00ff00)
        embed.add_field(name="Money", value=f"{self.db.balance(user.id)}")
        
        await interaction.response.send_message(user.mention, embed=embed)

    @app_commands.command(name="give", description="free robux giveaway!!!")
    async def give(self, interaction: discord.Interaction, user: discord.User, money: int):
        if not self.db.is_user(interaction.user.id):
            self.db.new_user(interaction.user.id)

        if not self.db.is_user(user.id):
            self.db.new_user(user.id)

        if self.db.balance(interaction.user.id) < money:
            await interaction.response.send_message(f"@everyone {user.mention} is a brokie")
            return

        self.db.add_money(interaction.user.id, -money)
        self.db.add_money(user.id, money)

        await interaction.response.send_message(":thumbs_up:")

    @app_commands.command(name="trade", description="eye for an eye")
    async def trade(self, interaction: discord.Interaction, user: discord.User, give_money: int = 0, give_monkeys: str = "", ask_money: int = 0, ask_monkeys: str = ""):
        if not self.db.is_user(interaction.user.id):
            self.db.new_user(interaction.user.id)

        if not self.db.is_user(user.id):
            self.db.new_user(user.id)

        if self.db.balance(interaction.user.id) < give_money:
            await interaction.response.send_message(f"@everyone {user.mention} is a brokie")
            return

        if self.db.balance(user.id) < ask_money:
            await interaction.response.send_message("the other mf too broke :skull:", ephemeral=True)
            return

        my_monkeys = self.db.get_monkeys(interaction.user.id)
        their_monkeys = self.db.get_monkeys(user.id)
        my_string = f"{ask_money}"
        their_string = f"{give_money}"

        for monkey in give_monkeys.split():
            if monkey not in my_monkeys:
                await interaction.response.send_message("you don't own me bitch!", ephemeral=True)
                return
                
            m = self.db.get_monkey(monkey)
            my_string += f"\n**{m[1]}** `#{monkey}`\n{m[2]}/{m[2]} :heart: {m[3]} :crossed_swords:"

        for monkey in ask_monkeys.split():
            if monkey not in their_monkeys:
                await interaction.response.send_message("they don't own it :sob:", ephemeral=True)
                return

            m = self.db.get_monkey(monkey)
            their_string += f"\n**{m[1]}** `#{monkey}`\n{m[2]}/{m[7]} :heart: {m[3]} :crossed_swords:"
        
        embed = discord.Embed(title="Trade offer")
        embed.add_field(name=f"{user.display_name} Gets", value=my_string)
        embed.add_field(name=f"{interaction.user.display_name} Gives", value=their_string)

        await interaction.response.send_message(f"{user.mention} {interaction.user.mention}", embed=embed, view=tradeViews(self.db, interaction.user, user, give_money, ask_money, give_monkeys.split(), ask_monkeys.split(), embed))

    @app_commands.command(name="monkeys", description="my collection!")
    async def monkeys(self, interaction: discord.Interaction, user: discord.User = None):
        if user is None:
            user = interaction.user

        if not self.db.is_user(user.id):
            self.db.new_user(user.id)

        collection = self.db.get_monkeys(user.id)
        
        embed = discord.Embed(title=f"{user.display_name}'s monkeys", color=0x00ff00)
        for m_id in collection:
            monkey = self.db.get_monkey(m_id)
            embed.add_field(name=f"{monkey[1]} `#{m_id}`", value=f"**{monkey[2]}/{monkey[7]} :heart:**\n**{monkey[3]} :crossed_swords:**")

        await interaction.response.send_message(user.mention, embed=embed)

    @app_commands.command(name="shop", description="trade!")
    async def shop (self, interaction: discord.Interaction):
        embed = discord.Embed(title="Shop", color=0x00ff00)
        for i in self.items.shop.keys():
            item = self.items.shop[i]
            embed.add_field(name=f"{i} - ${item['price']}", value=item['description'])
        
        await interaction.response.send_message(embed=embed)

async def setup(bot, db, monkeys, items):
    await bot.add_cog(Economy(bot, db, monkeys, items))