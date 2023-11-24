import discord, pymongo, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class setnick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Setnick Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"setnick"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"setnick"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="setnick", description="Sets a users nickname", aliases=['nick'])
    @commands.has_permissions(manage_nicknames=True)
    @commands.check(is_enabled)
    async def setnick(self, ctx, user: discord.Member = None, *, nick: str):
        if user == None:
            user = ctx.author
        await user.edit(nick=nick)
        await ctx.send(f"Set {user.mention}'s nickname to {nick}", ephemeral=True)

    @commands.hybrid_command(name="setnick", description="Sets a users nickname", aliases=['nick'])
    @commands.is_owner()
    async def setnick(self, ctx, user: discord.Member = None, *, nick: str):
        if user == None:
            user = ctx.author
        await user.edit(nick=nick)
        await ctx.send(f"Set {user.mention}'s nickname to {nick}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(setnick(bot))