import discord, pymongo, os
from discord.ext import commands
from pymongo import errors

from dotenv import load_dotenv

load_dotenv()

class warns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Warns Online")


    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"warns"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"warns"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="warn", description="Warn a user")
    @commands.has_permissions(manage_messages=True)
    @commands.check(is_enabled)
    async def warn(self, ctx, member:discord.Member, *, reason: str = None):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.warns
        embed = discord.Embed(title=f"{member.display_name} was warned!", description=f"The reason for this warn is for **{reason}**", color=ctx.author.color)
        await ctx.send(embed=embed)

        try:
            coll.insert_one({"_id":{"guild":member.guild.id, "user_id":member.id}, "count":1, "reason": reason})
        except pymongo.errors.DuplicateKeyError:
            coll.update_one({"_id":{"guild":member.guild.id, "user_id":member.id}}, {"$inc":{"count":1}})

    @commands.hybrid_command(name="warns", description="Check how many warns a user has")
    @commands.check(is_enabled)
    async def warns(self, ctx, member:discord.Member = None):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.warns

        if member == None:
            member = ctx.author

        if coll.find_one({"_id":{"guild":ctx.guild.id, "user_id":member.id}}):
            user = coll.find_one({"_id":{"guild":member.guild.id, "user_id":member.id}})
            embed = discord.Embed(title=f"Warns for {member.display_name}", description=f"{member.display_name} has **{user['count']}** warn(s)! Latest reason is for **{user['reason']}**", color=ctx.author.color)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"{member.display_name} has no warns!", color=ctx.author.color)
            await ctx.send(embed=embed)


    @commands.hybrid_command(name="clearwarns", description="Clear all warns from a user")
    @commands.has_permissions(manage_messages=True)
    @commands.check(is_enabled)
    async def clearwarns(self, ctx, member:discord.Member):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.warns
        coll.delete_one({"_id":{"guild":member.guild.id, "user_id":member.id}})
        embed = discord.Embed(title=f"{member.display_name} has been cleared of all warns!", color=ctx.author.color)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(warns(bot))