import discord, pymongo, os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

class leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leave Online")

    @commands.hybrid_command(name="leave", description="Leaves the guild")
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        # check through the entire database to see if the guild is in any of the collections and if it is, delete it
        for collection in db.list_collection_names():
            if db[collection].find_one({"_id": ctx.guild.id}):
                db[collection].delete_one({"_id": ctx.guild.id})
                await ctx.send("Deleted the guild from the database")

            else:
                return await ctx.send("No guild found in the database")

        await ctx.send("Left the guild")
        await ctx.guild.leave()

async def setup(bot):
    await bot.add_cog(leave(bot))