import discord, pymongo, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

class giverole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Giverole Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"giverole"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"giverole"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="giverole", description="Gives a user a role")
    @commands.has_permissions(administrator=True)
    async def giverole(self, ctx, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        await ctx.send(f"Gave {user.mention} the {role.name} role", ephemeral=True)

async def setup(bot):
    await bot.add_cog(giverole(bot))