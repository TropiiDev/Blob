import discord, aiohttp, pymongo, requests, os
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

class convo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"convosetup"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"convosetup"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.Cog.listener()
    async def on_ready(self):
        print("Convo Online")

    @commands.Cog.listener()
    async def on_message(self, message):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.convo

        if message.author == self.bot.user:
                return

        channel = coll.find_one({"_id": {"guild_id": message.guild.id}, "channel": message.channel.id})

        if channel == None:
            return
        
        else:
        
            if message.author == self.bot.user:
                return

            if channel:
                newchannel = channel['channel']
                channelll = self.bot.get_channel(newchannel)

            url = f"https://v6.rsa-api.xyz/ai/response?user_id=420&message={message.content}"

            headers = {
                "Authorization": "93FxvudCWXvO",
                "X-RapidAPI-Key": "5f878d0f8dmshe3320b9c7df0e88p1b8038jsnf03c5763a129",
                "X-RapidAPI-Host": "random-stuff-api.p.rapidapi.com"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://v6.rsa-api.xyz/ai/response?user_id=420&message={message.content}") as response:    
                    response = requests.request("GET", url, headers=headers)

            await channelll.send(response.json()['message'])

    @commands.hybrid_command(name="convosetup", description="Sets up a conversation channel")
    @commands.has_permissions(administrator=True)
    @commands.check(is_enabled)
    async def convosetup(self, ctx, channel: discord.TextChannel = None):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.convo

        if channel == None:
            channel = ctx.channel

        channell = coll.find_one({"_id": {"guild_id": ctx.guild.id}, "channel": channel.id})

        if channell == None:
            coll.insert_one({"_id": {"guild_id": ctx.guild.id}, "channel": channel.id})
            await ctx.send("Conversation channel setup!")

        else:
            await ctx.send("Conversation channel is already setup!")


async def setup(bot):
    await bot.add_cog(convo(bot))