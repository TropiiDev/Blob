import discord, pymongo, os
from discord.ext import commands

from dotenv import load_dotenv

class setuplist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("SetupList Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"setuplist"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"setuplist"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="setuplist", description="Find out all the commands that need setting up")
    @commands.has_permissions(administrator=True)
    @commands.check(is_enabled)
    async def setuplist(self, ctx):
        em = discord.Embed(title="Setup Commands List: ", description=None, color=ctx.author.color)
        em.add_field(name="convosetup", value="Continue with the setup options for convo", inline=False)
        em.add_field(name='asetup', value='Setup announcement channel', inline=False)

        await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(setuplist(bot))