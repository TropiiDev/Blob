import discord
import asyncio
import pymongo
import os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipe_message_content = None
        self.snipe_message_author = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Snipe Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"snipe"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"snipe"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.snipes

        channel = message.channel
        content = message.content
        author = message.author
        owner = self.bot.get_user(875604204889202698)

        if message.author.bot:
            return

        try:
            coll.insert_one({"_id": channel.id, "content": content, "author": author.id})
        except pymongo.errors.DuplicateKeyError:
            coll.update_one({"_id": channel.id}, {"$set": {"content": content, "author": author.id}})



    @commands.hybrid_command(name="snipe", description="Revive a deleted message")
    @commands.check(is_enabled)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def snipe(self, ctx, channel: discord.TextChannel = None):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.snipes

        if channel == None:
            channel = ctx.channel

        if coll.find_one({"_id": channel.id}):
            content = coll.find_one({"_id": channel.id})["content"]
            author = coll.find_one({"_id": channel.id})["author"]

            embed = discord.Embed(title="Sniped Message", description=f"**Author**: {self.bot.get_user(author).mention}\n**Content**: {content}", color=ctx.author.color)
            embed.set_thumbnail(url=self.bot.get_user(author).avatar)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send("There is nothing to snipe")

async def setup(bot):
    await bot.add_cog(Snipe(bot))