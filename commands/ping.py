import discord, typing, pymongo, os
from typing import Union
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"ping"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"ping"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping Online")

    @commands.hybrid_command(name="ping", description="Pong!")
    #@commands.check(is_enabled)
    async def ping(self, ctx):
        print("Ping Ping Ping")
        await ctx.send(f":ping_pong:**Pong!**\nLatency: {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(ping(bot))