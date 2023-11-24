import discord
from discord.ext import commands 

class guilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Guilds Online")

    @commands.hybrid_command(name="guilds", description="See how many guilds the bot is in")
    @commands.is_owner()
    async def guilds(self, ctx):
        for guild in self.bot.guilds:
            em = discord.Embed(title=str(guild), description=None, color=ctx.author.color)
            em.add_field(name="Owner: ", value=guild.owner, inline=False)
            em.add_field(name="Members: ", value=guild.member_count)
            await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(guilds(bot))