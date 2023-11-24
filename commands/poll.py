import discord, pymongo
from discord.ext import commands
import os

from dotenv import load_dotenv
load_dotenv()

class poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3',
                      '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001F51F']

    @commands.Cog.listener()
    async def on_ready(self):
        print("Poll Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"poll"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"poll"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="poll", description="Creates a poll")
    @commands.check(is_enabled)
    async def poll(self, ctx, title: str, *, options: str):
        options = options.split(',')
        if len(options) > 10:
            await ctx.send("You can only have 10 options!")

        else:
                polls = [('\u200b',
                        '\n'.join([f'{self.emoji[index]} {option} \n' for index, option in enumerate(options)]),
                          False)]

                embed = discord.Embed(title=title, description=None, colour=0xFF0000)

                embed.set_thumbnail(
                        url=ctx.author.avatar)

                for name, value, inline in polls:
                    embed.add_field(name=name, value=value, inline=inline)

                message = await ctx.send(embed=embed)

                for item in self.emoji[:len(options)]:
                    await message.add_reaction(item)
    
async def setup(bot):
    await bot.add_cog(poll(bot))