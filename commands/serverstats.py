import discord, pymongo, os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class serverstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ServerStats Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"serverstats"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"serverstats"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="serverstats", description="Check the servers stats")
    @commands.check(is_enabled)
    async def serverstats(self, ctx):
        role_count = len(ctx.guild.roles)

        em = discord.Embed(color = ctx.author.color)
        em.add_field(name="Server Name", value=f"{ctx.guild.name}", inline=False)
        em.add_field(name="Member Count", value=f"{ctx.guild.member_count}", inline=False)
        em.add_field(name="Verify Level", value=f"{ctx.guild.verification_level}", inline=False)
        em.add_field(name="Highest Role", value=f"{ctx.guild.roles[-1]}", inline=False)
        em.add_field(name="Number Of Roles", value=f"{role_count}", inline=False)
        em.add_field(name="Guild ID", value=f"{ctx.guild.id}", inline=False)
        await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(serverstats(bot))