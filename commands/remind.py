import discord, pymongo, asyncio, os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Remind Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"remind"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"remind"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="remind", description="Create a reminder")
    @commands.check(is_enabled)
    async def remind(self, ctx, time: int, *, reminder: str):
        em = discord.Embed(title="You will be reminded about: ", description=f"{reminder} in {time} hours", color=ctx.author.color)
        await ctx.send(embed=em)
        await asyncio.sleep(time*3600)
        em1 = discord.Embed(title="Reminder", description=f"{ctx.author.mention}, you asked me to remind you about: {reminder}", color=ctx.author.color)
        await ctx.send(embed=em1)

async def setup(bot):
    await bot.add_cog(remind(bot))