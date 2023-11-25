# LINKED WITH ECONOMY.PY
import discord, asyncio, pymongo, os
from discord.ext import commands
from dotenv import load_dotenv
from discord.ui import Button, button, View

from dotenv import load_dotenv
load_dotenv()

def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"ticket"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"ticket"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

class BronzeButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SilverButton())
        self.add_item(GoldButton())
        self.add_item(DiamondButton())
        self.add_item(EmeraldButton())

    @button(label="Buy Bronze", style=discord.ButtonStyle.blurple, custom_id="bronze")
    async def bronze(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy

        cost = 100
        guild = interaction.guild
        user = interaction.user

        userColl = coll.find_one({"_id": {'author_id': user.id, 'guild_id': guild.id}})

        if not userColl:
            await interaction.followup.send("You don't have any coins!", ephemeral=True)
            return
        
        if userColl["coins"] < cost:
            await interaction.followup.send("You don't have enough coins!", ephemeral=True)
            return
        
        if userColl["coins"] >= cost:
            coll.update_one({"_id": {'author_id': user.id, 'guild_id': guild.id}}, {"$inc":{"coins":-cost}})
            coll.update_one({"_id": {"author_id": user.id, "guild_id": guild.id}}, {"$set": {"bought": "bronze"}})
            await interaction.followup.send("You bought the bronze ticket! Redeem it in the Blob support server for rewards!", ephemeral=True)
            return
        
class SilverButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Buy Silver", style=discord.ButtonStyle.blurple, custom_id="silver")
    async def bronze(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy

        cost = 200
        guild = interaction.guild
        user = interaction.user

        userColl = coll.find_one({"_id": {'author_id': user.id, 'guild_id': guild.id}})

        if not userColl:
            await interaction.followup.send("You don't have any coins!", ephemeral=True)
            return
        
        if userColl["coins"] < cost:
            await interaction.followup.send("You don't have enough coins!", ephemeral=True)
            return
        
        if userColl["coins"] >= cost:
            coll.update_one({"_id": {'author_id': user.id, 'guild_id': guild.id}}, {"$inc":{"coins":-cost}})
            coll.update_one({"_id": {"author_id": user.id, "guild_id": guild.id}}, {"$set": {"bought": "silver"}})
            await interaction.followup.send("You bought the silver ticket! Redeem it in the Blob support server for rewards!", ephemeral=True)
            return

class GoldButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Buy Gold", style=discord.ButtonStyle.blurple, custom_id="gold")
    async def bronze(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy

        cost = 400
        guild = interaction.guild
        user = interaction.user

        userColl = coll.find_one({"_id": {'author_id': user.id, 'guild_id': guild.id}})

        if not userColl:
            await interaction.followup.send("You don't have any coins!", ephemeral=True)
            return
        
        if userColl["coins"] < cost:
            await interaction.followup.send("You don't have enough coins!", ephemeral=True)
            return
        
        if userColl["coins"] >= cost:
            coll.update_one({"_id": {'author_id': user.id, 'guild_id': guild.id}}, {"$inc":{"coins":-cost}})
            coll.update_one({"_id": {"author_id": user.id, "guild_id": guild.id}}, {"$set": {"bought": "gold"}})
            await interaction.followup.send("You bought the gold ticket! Redeem it in the Blob support server for rewards!", ephemeral=True)
            return
        
class DiamondButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Buy Diamond", style=discord.ButtonStyle.blurple, custom_id="diamond")
    async def bronze(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy

        cost = 800
        guild = interaction.guild
        user = interaction.user

        userColl = coll.find_one({"_id": {'author_id': user.id, 'guild_id': guild.id}})

        if not userColl:
            await interaction.followup.send("You don't have any coins!", ephemeral=True)
            return
        
        if userColl["coins"] < cost:
            await interaction.followup.send("You don't have enough coins!", ephemeral=True)
            return
        
        if userColl["coins"] >= cost:
            coll.update_one({"_id": {'author_id': user.id, 'guild_id': guild.id}}, {"$inc":{"coins":-cost}})
            coll.update_one({"_id": {"author_id": user.id, "guild_id": guild.id}}, {"$set": {"bought": "diamond"}})
            await interaction.followup.send("You bought the diamond ticket! Redeem it in the Blob support server for rewards!", ephemeral=True)
            return
        
class EmeraldButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Buy Emerald", style=discord.ButtonStyle.blurple, custom_id="emerald")
    async def bronze(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy

        cost = 1600
        guild = interaction.guild
        user = interaction.user

        userColl = coll.find_one({"_id": {'author_id': user.id, 'guild_id': guild.id}})

        if not userColl:
            await interaction.followup.send("You don't have any coins!", ephemeral=True)
            return
        
        if userColl["coins"] < cost:
            await interaction.followup.send("You don't have enough coins!", ephemeral=True)
            return
        
        if userColl["coins"] >= cost:
            coll.update_one({"_id": {'author_id': user.id, 'guild_id': guild.id}}, {"$inc":{"coins":-cost}})
            coll.update_one({"_id": {"author_id": user.id, "guild_id": guild.id}}, {"$set": {"bought": "emerald"}})
            await interaction.followup.send("You bought the emerald ticket! Redeem it in the Blob support server for rewards!", ephemeral=True)
            return

class store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Tickets Online')

    @commands.hybrid_command(name="store", description="View the store")
    @commands.has_permissions(administrator=True)
    @commands.check(is_enabled)
    async def ticket(self, ctx):
        em = discord.Embed(title="Shop!", description="Spend some Bloboons to get cool rewards! Redeem in supported servers!", color=ctx.author.color)
        em.add_field(name="Bronze Ticket", value="100 Bloboons", inline=False)
        em.add_field(name="Silver Ticket", value="200 Bloboons", inline=False)
        em.add_field(name="Gold Ticket", value="400 Bloboons", inline=False)
        em.add_field(name="Diamond Ticket", value="800 Bloboons", inline=False)
        em.add_field(name="Emerald Ticket", value="1600 Bloboons", inline=False)

        await ctx.send(
            embed=em,
            view=BronzeButton()
            #view=SilverButton(),
            #view=GoldButton(),
            #view=DiamondButton(),
            #view=EmeraldButton()
        )

async def setup(bot):
    await bot.add_cog(store(bot))
