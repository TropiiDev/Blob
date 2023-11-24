import discord, pymongo, os
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

class cookie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cookie Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"cookie"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"cookie"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="cookie", description="Recieve a cookie")
    @commands.check(is_enabled)
    async def cookie(self, ctx):
        await ctx.send("Here you go, take a cookie")


async def setup(bot):
    await bot.add_cog(cookie(bot))