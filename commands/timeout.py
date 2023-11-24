import discord, pymongo, datetime, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Timeout Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"timeout"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"timeout"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="timeout", description="Timeout a user")
    @commands.has_permissions(manage_messages=True)
    @commands.check(is_enabled)
    async def timeout(self, ctx, user: discord.Member, time: int, reason: str = None):
        if user == ctx.author:
            await ctx.send("You can't timeout yourself silly")
        else:
            await user.timeout(datetime.timedelta(minutes=time), reason=reason)
            await ctx.send(f"{user.mention} has been timed out for {reason}", ephemeral=True)

    @commands.hybrid_command(name="removetimeout", description="Remove a users timeout", aliases=['rt'])
    @commands.has_permissions(manage_messages=True)
    @commands.check(is_enabled)
    async def removetimeout(self, ctx, user: discord.Member):
        await user.timeout(None)
        await ctx.send(f"{user.mention} has been removed from timeout", ephemeral=True)

async def setup(bot):
    await bot.add_cog(timeout(bot))