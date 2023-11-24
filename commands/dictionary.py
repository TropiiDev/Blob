import discord, pymongo, aiohttp, os
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

class dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Dictionary Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"dictionary"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"dictionary"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="dictionary", description="Searches a word in the dictionary")
    @commands.check(is_enabled)
    async def dictionary(self, ctx, *, term: str):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term":term}

        headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': "5f878d0f8dmshe3320b9c7df0e88p1b8038jsnf03c5763a129"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                r = await response.json()
                definition = r['list'][0]['definition']
                embed = discord.Embed(title=f"First result for: {term}", description=None)
                embed.add_field(name=term, value=definition, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(dictionary(bot))