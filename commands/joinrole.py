import discord, pymongo, os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"joinrole"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"joinrole"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True
        
class joinrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Joinrole Online")

    @commands.hybrid_command(name="joinrole", description="Set the joinrole")
    @commands.check(is_enabled)
    @commands.has_permissions(manage_roles=True)
    async def joinrole(self, ctx, role:discord.Role):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.roles
        roles = coll.find_one({"_id": {"guild_id": ctx.guild.id}})
        if not roles:
            coll.insert_one({"_id": {"guild_id": ctx.guild.id}, "joinrole": role.id})
            await ctx.send(f"Set the joinrole to {role.mention}!")
            return
        else:
            coll.update_one({"_id": {"guild_id": ctx.guild.id}}, {"$set": {"joinrole": role.id}})

        await ctx.send(f"Set the joinrole to {role.mention}!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.roles

        joinrole = coll.find_one({"_id": {"guild_id": member.guild.id}})
        if joinrole:
            role = member.guild.get_role(joinrole["joinrole"])
            await member.add_roles(role)

async def setup(bot):
    await bot.add_cog(joinrole(bot))