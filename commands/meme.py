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
        url = "https://humor-jokes-and-memes.p.rapidapi.com/memes/random"

        querystring = {"number":"1","media-type":"image","keywords-in-image":"false","min-rating":"4"}

        headers = {
            "X-RapidAPI-Key": "fc3dac086bmsh835062c787b309ep1c9d10jsnf9716a0fe3fb",
	        "X-RapidAPI-Host": "humor-jokes-and-memes.p.rapidapi.com"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get("https://reddit-meme.p.rapidapi.com/memes/trending") as response:    
                response = requests.request("GET", url, headers=headers)

                json_data = json.loads(response.text)
                description = json_data["description"]
                url = json_data["url"]

                embed = discord.Embed(
                    title="Meme",
                    description=description,
                    color=ctx.author.color
                )
                embed.set_image(url=url)
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(meme(bot))