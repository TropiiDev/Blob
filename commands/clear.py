import discord, pymongo, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Clear Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"clear"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"clear"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="clear", description="Bulk deletes messages")
    @commands.has_permissions(manage_messages=True)
    @commands.check(is_enabled)
    async def clear(self, ctx, amount: int):
        await ctx.send(f"Deleted {amount} messages", ephemeral=True, delete_after=2)
        await ctx.channel.purge(limit=amount)

    @commands.hybrid_command(name="oclear", description="Bulk deletes messages but only tropii can use it")
    @commands.is_owner()
    async def oclear(self, ctx, amount: int):
        await ctx.send(f"Deleted {amount} messages", ephemeral=True, delete_after=2)
        await ctx.channel.purge(limit=amount)

async def setup(bot):
    await bot.add_cog(clear(bot))
