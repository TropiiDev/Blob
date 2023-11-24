import discord, pymongo, os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Remove Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"remove"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"remove"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="remove", description="Remove a role from a user")
    @commands.has_permissions(administrator=True)
    @commands.check(is_enabled)
    async def remove(self, ctx, user: discord.Member, role: discord.Role):
        await user.remove_roles(role)
        await ctx.send(f"Removed {role} from {user.display_name}")


async def setup(bot):
    await bot.add_cog(remove(bot))