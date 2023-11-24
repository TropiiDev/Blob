import discord, pymongo, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class membercount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Membercount Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"membercount"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"membercount"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True
    
    @commands.hybrid_command(name="membercount", description="Shows the membercount", aliases=['mc'])
    @commands.check(is_enabled)
    async def membercount(self, ctx):
        em = discord.Embed(title="Member Count", description=f"Total Members: {ctx.guild.member_count}", color=ctx.author.color)
        await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(membercount(bot))