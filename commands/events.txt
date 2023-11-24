from typing import Optional
import discord, pymongo, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Online")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.prefixes

        coll.insert_one({"_id":guild.id, "prefix":"-"})

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.prefixes

        coll.delete_one({"_id":guild.id})

async def setup(bot):
    await bot.add_cog(events(bot))