import discord, pymongo, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class roleinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Roleinfo Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"roleinfo"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"roleinfo"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="roleinfo", description="Get info about a role")
    @commands.check(is_enabled)
    async def roleinfo(self, ctx, role: discord.Role):
        embed = discord.Embed(title=role.name, color=role.color)
        embed.add_field(name="ID", value=role.id, inline=False)
        embed.add_field(name="Color", value=role.color, inline=False)
        embed.add_field(name="Position", value=role.position, inline=False)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=False)
        embed.add_field(name="Hoisted", value=role.hoist, inline=False)
        embed.add_field(name="Managed", value=role.managed, inline=False)
        embed.add_field(name="Created At", value=role.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Members", value=len(role.members), inline=False)
        embed.set_thumbnail(url=role.guild.icon)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(roleinfo(bot))