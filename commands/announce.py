import discord, pymongo, asyncio, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Announce Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"announce"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"announce"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="asetup", description="Setup the announce command")
    @commands.has_permissions(administrator=True)
    async def asetup(self, ctx, channel: discord.TextChannel):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.announce

        if coll.find_one({"_id": {"guild_id": ctx.guild.id}}):
            await ctx.send("You have already made an announcement channel")
            await ctx.send("If you would like to delete this setting please say 'delete' in the next 10 seconds")

            # if the user says delete, then delete the entry in the database
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=10)
                if msg.content == "delete":
                    a = coll.find_one({"_id": {"guild_id": ctx.guild.id}})
                    b = a["channel"]
                    coll.delete_one({"_id": {"guild_id": ctx.guild.id}, channel: b})
                    await ctx.send("Deleted the announcement channel")
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond")
                return
        
        else:
            coll.insert_one({"_id": {"guild_id": ctx.guild.id}, "channel": channel.id})
            await ctx.send("Announcement channel set")

    @commands.hybrid_command(name="announce", description="Announce something")
    @commands.has_permissions(administrator=True)
    @commands.check(is_enabled)
    async def announce(self, ctx, *, message):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.announce

        ak = coll.find_one({"_id": {"guild_id": ctx.guild.id}})

        await ctx.send(ak)


        if coll.find_one({"_id": {"guild_id": ctx.guild.id}}):
            channel = coll.find_one({"_id": {"guild_id": ctx.guild.id}, "channel": ctx.channel.id})
            if channel == False:
                await ctx.send("You can only use this command in the announcement channel")
                return
            else:
                newchannel = channel['channel']
                channelll = self.bot.get_channel(newchannel)
                await channelll.send(message)
                await ctx.send("Announcement sent", delete_after=2)

        else:
            await ctx.send("You have not set an announcement channel yet")
            

async def setup(bot):
    await bot.add_cog(announce(bot))