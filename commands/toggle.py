import discord, pymongo, os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class toggle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Toggle Online")

    @commands.hybrid_command(name="toggle", description="Toggles a command", aliases=["t"])
    @commands.has_permissions(administrator=True)
    async def toggle(self, ctx, command_name: str, enabled: bool):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings
        # convert command_name to lowercase
        command = command_name.lower()
        ## check if command exists
        for c in self.bot.commands:
            if c.name == command:
                return True
            
            if c.name == "toggle":
                await ctx.send("You can't disable the toggle command!")
                break

            ## check if the command is in the database
            if coll.find_one({"_id": {"guild_id": ctx.guild.id, "commands":command}}):
                coll.update_one({"_id": {"guild_id": ctx.guild.id, "commands":command}}, {"$set":{"enabled":enabled}})
                embed = discord.Embed(title=f"{command_name} has been toggled to {enabled}", color=ctx.author.color)
                await ctx.send(embed=embed)
                break
            else:
                coll.insert_one({"_id": {"guild_id": ctx.guild.id, "commands":command}, "enabled":enabled})
                embed = discord.Embed(title=f"{command_name} has been toggled to {enabled}", color=ctx.author.color)
                await ctx.send(embed=embed)
                break
        else:
            embed = discord.Embed(title=f"{command} is not a valid command!", color=ctx.author.color)
            await ctx.send(embed=embed)
            print("------")
            print(self.bot.commands)

async def setup(bot):
    await bot.add_cog(toggle(bot))