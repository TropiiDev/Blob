import discord, pymongo, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slowmode Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"slowmode"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"slowmode"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="slowmode", description="Set the channels slowmode")
    @commands.has_permissions(manage_channels=True)
    @commands.check(is_enabled)
    async def slowmode(self, ctx, seconds: int = None, *, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        if seconds == None:
            await channel.edit(slowmode_delay=0)
            await ctx.send(f"Slowmode in {channel.mention} has been disabled.")
        else:
            await channel.edit(slowmode_delay=seconds)
            await ctx.send(f"Set the slowmode of {channel.mention} to {seconds} seconds")

async def setup(bot):
    await bot.add_cog(slowmode(bot))
