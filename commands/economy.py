import discord, pymongo, random, os
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy Online")

    @commands.hybrid_command(name="beg", description="Beg for money")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy
        num = random.randint(1, 100)
        try:
            coll.insert_one({"_id": {'author_id': ctx.author.id, 'guild_id': ctx.guild.id}, "coins":num})
            await ctx.send(f"{ctx.author.mention} begged for money and got {num} bloboons!")
        except pymongo.errors.DuplicateKeyError:
            coll.update_one({"_id": {'author_id': ctx.author.id, 'guild_id': ctx.guild.id}}, {"$inc":{"coins":num}})
            await ctx.send(f"{ctx.author.mention} begged for money and got {num} bloboons!")

    @commands.hybrid_command(name="balance", description="Check your balance", aliases=["bal"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def balance(self, ctx, member:discord.Member = None):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy
        if member == None:
            member = ctx.author
        users = coll.find({})
        for user in users:
            if user["_id"]["author_id"] == member.id and user["_id"]["guild_id"] == ctx.guild.id:
                await ctx.send(f"{member.mention} has {user['coins']} coins!")
                return
        await ctx.send(f"{member.mention} has 0 bloboons!")

    @commands.hybrid_command(name="pay", description="Pay someone")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def pay(self, ctx, member:discord.Member, amount:int):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy
        users = coll.find({})
        for user in users:
            if user["_id"]["author_id"] == ctx.author.id and user["_id"]["guild_id"] == ctx.guild.id:
                if user["coins"] < amount:
                    await ctx.send("You don't have enough bloboons!")
                    return
                coll.update_one({"_id": {'author_id': ctx.author.id, 'guild_id': ctx.guild.id}}, {"$inc":{"coins":-amount}})
                for user in users:
                    if user["_id"]["author_id"] == member.id and user["_id"]["guild_id"] == ctx.guild.id:
                        coll.update_one({"_id": {'author_id': member.id, 'guild_id': ctx.guild.id}}, {"$inc":{"coins":amount}})
                        await ctx.send(f"You paid {member.mention} {amount} bloboons!")
                        return
                coll.insert_one({"_id": {'author_id': member.id, 'guild_id': ctx.guild.id}, "coins":amount})
                await ctx.send(f"You paid {member.mention} {amount} bloboons!")
                return

    @commands.hybrid_command(name="work", description="Work for money")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def work(self, ctx):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy
        num = random.randint(1, 500)
        try:
            coll.insert_one({"_id": {'author_id': ctx.author.id, 'guild_id': ctx.guild.id}, "coins":num})
            await ctx.send(f"{ctx.author.mention} worked for money and got {num} bloboons!")
        except pymongo.errors.DuplicateKeyError:
            coll.update_one({"_id": {'author_id': ctx.author.id, 'guild_id': ctx.guild.id}}, {"$inc":{"coins":num}})
            await ctx.send(f"{ctx.author.mention} worked for money and got {num} bloboons!")
        
    @commands.hybrid_command(name="rob", description="Rob someone")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, member:discord.Member):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy
        users = coll.find({})
        for user in users:
            if user["_id"]["author_id"] == ctx.author.id and user["_id"]["guild_id"] == ctx.guild.id:
                if user["coins"] < 100:
                    await ctx.send("You don't have enough bloboons!")
                    return
                for user in users:
                    if user["_id"]["author_id"] == member.id and user["_id"]["guild_id"] == ctx.guild.id:
                        if user["coins"] < 100:
                            await ctx.send("They don't have enough bloboons!")
                            return
                        num = random.randint(1, 100)
                        if num > 50:
                            coll.update_one({"_id": {'author_id': ctx.author.id, 'guild_id': ctx.guild.id}}, {"$inc":{"coins":100}})
                            coll.update_one({"_id": {'author_id': member.id, 'guild_id': ctx.guild.id}}, {"$inc":{"coins":-100}})
                            await ctx.send(f"You robbed {member.mention} and got 100 bloboons!")
                            return
                        coll.update_one({"_id": {'author_id': ctx.author.id, 'guild_id': ctx.guild.id}}, {"$inc":{"coins":-100}})
                        await ctx.send(f"You failed to rob {member.mention} and lost 100 bloboons!")
                        return
                await ctx.send("They don't have an account!")
                return

    @commands.hybrid_command(name="slots", description="Play slots")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def slots(self, ctx, amount:int):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy
        users = coll.find({})
        num = random.randint(1, 1000)
        for user in users:
            if user["_id"]["author_id"] == ctx.author.id and user["_id"]["guild_id"] == ctx.guild.id:
                if user["coins"] < amount:
                    await ctx.send("You don't have enough bloboons!")
                    return
                if num > 50:
                    coll.update_one({"_id": {'author_id': ctx.author.id, 'guild_id': ctx.guild.id}}, {"$inc":{"coins":num}})
                    await ctx.send(f"You won {num} bloboons!")
                    return
                coll.update_one({"_id": {'author_id': ctx.author.id, 'guild_id': ctx.guild.id}}, {"$inc":{"coins":-amount}})
                await ctx.send(f"You lost {amount} bloboons!")
                return

    @commands.hybrid_command(name="eleaderboard", description="View the leaderboard", aliases=["elb"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def eleaderboard(self, ctx):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.economy
        users = coll.find({})
        users = sorted(users, key=lambda x: x["coins"], reverse=True)
        embed = discord.Embed(title="Leaderboard", description="The top 10 richest people in the server", color=discord.Color.blue())
        for i in range(10):
            embed.add_field(name=f"{i+1}. {ctx.guild.get_member(users[i]['_id']['author_id']).name}", value=f"{users[i]['coins']} bloboons", inline=False)
        await ctx.send(embed=embed)
            

async def setup(bot):
    await bot.add_cog(economy(bot))