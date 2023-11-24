import discord, pymongo, os
from discord import app_commands
from discord.ext import commands
from discord.utils import get

from dotenv import load_dotenv

load_dotenv()

# local imports
import ext.guildid as guildid
from ext.afks import afks

def remove(afk):
    if "[AFK]" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"afk"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"afk"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("AFK Online")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick=remove(message.author.display_name))
            except:
                pass
            await message.channel.send(f"{message.author.mention} is no longer AFK")
        
        for id, reason in afks.items():
            if id == self.bot.user.id:
                return
            member = get(message.guild.members, id=id)
            if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                await message.reply(f"{member.display_name} is AFK: {reason}")

    @commands.hybrid_command(name="afk", description="Set your status to AFK - not hidden from members")
    @commands.check(is_enabled)
    async def afk(self, ctx, *, reason:str = None):
        if ctx.author.id in afks.keys():
            afks.pop(ctx.author.id)
        else: 
            try:
                await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
            except:
                pass

        afks[ctx.author.id] = reason
        em = discord.Embed(title=f":zzz: Member AFK", description=f"{ctx.author.mention} has went AFK", color=0x00ff00)
        em.set_thumbnail(url=ctx.author.avatar)
        em.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
        em.add_field(name="AFK Note: ", value=reason)
        em.set_footer(text=f"Powered by {self.bot.user.name}", icon_url=self.bot.user.avatar)
        await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(afk(bot))