import discord, pymongo
from discord import app_commands
from discord.ext import commands

class kb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("KBU Online")

    @commands.hybrid_command(name="kick", description="Kicks a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if member == ctx.author:
            await ctx.send("You can't kick yourself stupid")
        else:
            guild = ctx.guild
            em = discord.Embed(title="Kick", description=f"{member.mention} has been kicked for {reason}", color = ctx.author.color)
            emmember = discord.Embed(title="Kicked", description=f"You have been kicked in {guild.name} for {reason}", color = ctx.author.color)
            await ctx.send(embed=em)
            await member.send(embed=emmember)
            await member.kick(reason=reason)
        

    @commands.hybrid_command(name="ban", description="Bans a user", aliases=['b', 'banish', 'banhammer', 'hammer', 'hammer tim'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if member == ctx.author:
            await ctx.send("No can do pal")
        else:
            ctxem = discord.Embed(title="Ban", description=f"{member.mention} has been banned in the server for {reason}", color = ctx.author.color)
            await member.ban(reason=reason)
            await ctx.send(embed=ctxem)

async def setup(bot):
    await bot.add_cog(kb(bot))