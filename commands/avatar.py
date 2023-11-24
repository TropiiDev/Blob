import discord, pymongo, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

class avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"avatar"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"avatar"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("Avatar Online")

    @commands.hybrid_command(name="avatar", description="Shows a users avatar", aliases=['av'])
    async def avatar(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        em = discord.Embed(title=f"{user.name}'s Avatar", color=user.color)
        em.set_image(url=user.avatar)
        await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(avatar(bot))