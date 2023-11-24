import discord, pymongo, requests, aiohttp, json, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Meme Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"meme"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"meme"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="meme", description="Shows a random meme")
    @commands.check(is_enabled)
    async def meme(self, ctx):
        url = "https://reddit-meme.p.rapidapi.com/memes/trending"

        headers = {
            "X-RapidAPI-Key": "5f878d0f8dmshe3320b9c7df0e88p1b8038jsnf03c5763a129",
	        "X-RapidAPI-Host": "reddit-meme.p.rapidapi.com"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get("https://reddit-meme.p.rapidapi.com/memes/trending") as response:    
                response = requests.request("GET", url, headers=headers)

                json_data = json.loads(response.text)
                title = json_data[1]
                await ctx.send(title)
                image = json_data[2]
                em = discord.Embed(title=title, color=ctx.author.color)
                em.set_image(url=image)
                await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(meme(bot))