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

    @button(label="Buy Bronze", style=discord.ButtonStyle.blurple, custom_id="bronze")
    async def bronze(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy

        cost = 100
        guild = interaction.guild
        user = interaction.user 

        user = coll.find_one({"_id": {'author_id': user.id, 'guild_id': guild.id}})

        if not user:
            await interaction.followup.send("You don't have any coins!", ephemeral=True)
            return
        
        if user["coins"] < cost:
            await interaction.followup.send("You don't have enough coins!", ephemeral=True)
            return
        
        if user["coins"] >= cost:
            coll.update_one({"_id": {'author_id': user.id, 'guild_id': guild.id}}, {"$inc":{"coins":-cost}})
            coll.update_one({"_id": {"author_id": user.id, "guild_id": guild.id}}, {"$set": {"bought": "bronze"}})
            await interaction.followup.send("You bought the bronze ticket! Redeem it in the Blob support server for rewards!", ephemeral=True)
            return

class store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Tickets Online')

    @commands.hybrid_command(name="ticket", description="Create a ticket")
    @commands.has_permissions(administrator=True)
    @commands.check(is_enabled)
    async def ticket(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                description="Shop!",
                color=ctx.author.color
            ),
            view=BronzeButton()
        )

async def setup(bot):
    await bot.add_cog(store(bot))
