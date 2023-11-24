import discord, random, pymongo, os
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

class flip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Flip Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"flip"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"flip"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="flip", description="Flip a coin")
    async def flip(self, ctx):
        num = [
            '1',
            '2'
        ]
        flipnum = random.choice(num)
        if flipnum == '1':
            await ctx.send("Heads!!")
        elif flipnum == "2":
            await ctx.send("Tails!!")


async def setup(bot):
    await bot.add_cog(flip(bot))