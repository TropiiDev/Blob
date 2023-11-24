import discord, random, pymongo, os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class rnum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Rnum Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"rnum"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"rnum"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="rnum", description="Get a random number between from what you choose", aliases=["rn"])
    @commands.check(is_enabled)
    async def rnum(self, ctx, num1: int, num2: int):
        await ctx.send(f"{random.randint(num1, num2)}")


async def setup(bot):
    await bot.add_cog(rnum(bot))