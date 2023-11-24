import discord, pymongo, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

class lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Lockdown Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"lockdown"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"lockdown"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="lockdown", description="Lockdown a channel", aliases=['ld', 'lock'])
    @commands.has_permissions(manage_channels=True)
    @commands.check(is_enabled)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"{channel.mention} has been locked down", ephemeral=True)

    @commands.hybrid_command(name="unlock", description="Unlock a channel")
    @commands.has_permissions(manage_channels=True)
    @commands.check(is_enabled)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"{channel.mention} has been unlocked", ephemeral=True)

async def setup(bot):
    await bot.add_cog(lockdown(bot))