import discord, pymongo, os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Info Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"info"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"info"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="info", description="Shows info about the user")
    @commands.check(is_enabled)
    async def info(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        em = discord.Embed(title=f"{user.name}'s Info", description=f"Shows info about {user.name}", color=user.color)
        em.add_field(name="Name", value=user.name, inline=False)
        em.add_field(name="ID", value=user.id, inline=False)
        em.add_field(name="Status", value=user.status, inline=False)
        em.add_field(name="Top Role", value=user.top_role.mention, inline=False)
        em.add_field(name="Joined At", value=user.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
        em.add_field(name="Created At", value=user.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
        em.set_thumbnail(url=user.avatar)

        await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(info(bot))