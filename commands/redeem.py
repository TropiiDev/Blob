import discord, pymongo, os
from discord.ext import commands

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

class redeem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Redeem Online")

    @commands.hybrid_command(name="redeem", description="Redeem a ticket")
    @commands.check(is_enabled)
    async def redeem(self, ctx, ticket_type: str):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy

        guild = ctx.guild
        user = ctx.author

        userColl = coll.find_one({"_id": {'author_id': user.id, 'guild_id': guild.id}})
        if not userColl:
            await ctx.send("You don't have any coins!")
            return
        
        if not userColl["bought"]:
            await ctx.send("You don't have any tickets!")
            return
        
        if ticket_type == userColl["bought"]:
            coll.update_one({"_id": {"author_id": user.id, "guild_id": guild.id}}, {"$set": {"bought": None}})
            await ctx.send("You redeemed your ticket!")
            return
        
        else:
            await ctx.send("You don't have that ticket!")
            return
        
async def setup(bot):
    await bot.add_cog(redeem(bot))