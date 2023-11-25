import discord, pymongo, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Staff Commands", emoji="🚫", description="Look at all the staff commands"),
            discord.SelectOption(label="Normal Commands", emoji="👍", description="Look at all the normal commands")
        ]
        super().__init__(custom_id="helpSelect", placeholder="Choose the commands you want to view", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Staff Commands":
            em = discord.Embed(title="Staff Commands", description="Here are all the staff commands", color=interaction.user.color)
            em.add_field(name="announce", value="Announce a message in the Announcements channel, Example: -announce Announcing a message", inline=False)
            em.add_field(name="clear", value="Bulk deletes messages, Example: -clear 5", inline=False)
            em.add_field(name="kick", value="Kicks a member from the server, Example: -kick @Tropiiツ", inline=False)
            em.add_field(name="ban", value="Ban a member from the server, Example: -ban @Tropiiツ", inline=False)
            em.add_field(name="mute", value="Mutes a member, Example: -mute @Tropiiツ", inline=False)
            em.add_field(name="timeout", value="Timeout a member for some time, Example: -timeout @Tropiiツ 5 (It will timeout someone for 5 minutes)", inline=False)
            em.add_field(name="warn", value="Warn a member, Example: -warn @Tropiiツ being amazing", inline=False)
            em.add_field(name="giverole", value="Give someone a role, Example: -giverole @Tropiiツ @Moderator", inline=False)
            em.add_field(name="unmute", value="Un mutes someone, Example: -unmute @Tropiiツ", inline=False)
            em.add_field(name="setnick", value="Changes someones nickname, Example: -setnick @Tropiiツ Tropii", inline=False)
            em.add_field(name="clearwarns", value="Clear someones warnings, Example: -clearwarns @Tropiiツ", inline=False)
            em.add_field(name="removetimeout", value="Remove someones timeout, Example: -removetimeout @Tropiiツ", inline=False)
            em.add_field(name="slowmode", value="Set a channels slowmode, Example: -slowmode 2 (Will set the slowmode to 2 seconds)", inline=False)
            em.add_field(name="lockdown", value="Lockdown a channel so members can't type in it, Example: -lockdown", inline=False)
            em.add_field(name="unlock", value="Unlocks a channel, Example: -unlock", inline=False)
            em.add_field(name="trash", value="Delete a ticket, Example: -trash", inline=False)
            em.add_field(name="remove", value="Removes a role from a user, Example: -remove @Tropiiツ @Owner", inline=False)
            em.add_field(name="joinrole", value="Set the role a user gets on join, Example: -joinrole @Member", inline=False)
            await interaction.response.send_message(embed=em, ephemeral=True)
        elif self.values[0] == "Normal Commands":
            em1 = discord.Embed(title="Normal Commands", description="Here are all the normal commands", color=interaction.user.color)
            em1.add_field(name="help", value="See this message, Example: -help", inline=False)
            em1.add_field(name="ping", value="Show the bots latency, Example: -ping", inline=False)
            em1.add_field(name="warns", value="Show a yours or a members warns, Example: -warns or -warns @Tropiiツ", inline=False)
            em1.add_field(name="info", value="Check a members info, Example: -info or -info @Tropiiツ", inline=False)
            em1.add_field(name="avatar", value="See a users avatar, Example: -avatar or -av @Tropiiツ", inline=False)
            em1.add_field(name="membercount", value="See how many members are in a server, Example: -membercount", inline=False)
            em1.add_field(name="meme", value="Look at a horrible meme, Example: -meme", inline=False)
            em1.add_field(name="poll", value="Create a poll, Example: -poll 'Amazing Poll' Question1 Question2", inline=False)
            em1.add_field(name="afk", value="Become AFK, Example: -afk", inline=False)
            em1.add_field(name="dictionary", value="Look in the urban dictionary for a word, WARNING: If the bot responds with a error do not mention me or anything about it there is nothing wrong with the bot the word just isn't in the dictionary, Example: -dictionary Hello", inline=False)
            em1.add_field(name="roleinfo", value="Get info about a role, Example: -roleinfo @Moderator", inline=False)
            em1.add_field(name="ticket", value="Create a ticket, Example: -ticket I need help", inline=False)
            em1.add_field(name="close", value="Close a ticket, Example: -close", inline=False)
            em1.add_field(name="serverstats", value="Check and see the server stats!", inline=False)
            em1.add_field(name="flip", value="Flip a coin and get heads or tails! Example: -flip", inline=False)
            em1.add_field(name="remind", value="Remind yourself about something, WARNING: It lasts 1 hour, Example: -remind 1 this will last one hour", inline=False)
            em1.add_field(name="omokoko", value="Custom Command requested by Woole. Example: -omokoko", inline=False)
            em1.add_field(name="cookie", value="Custom Command requested by Cookie, Example: -cookie", inline=False)
            em1.add_field(name="story", value="Read a nice story, Example: -story", inline=False)
            em1.add_field(name="rnum", value="The bot chooses a random number, Example: -rnum 1 5 (Will choose a number between 1 and 5)", inline=False)
            em1.add_field(name="beg", value="Beg for money, Example: -beg", inline=False)
            em1.add_field(name="work", value="Work for money, Example: -work", inline=False)
            em1.add_field(name="balance", value="Check your balance, Example: -balance", inline=False)
            em1.add_field(name="pay", value="Pay someone money, Example: -pay @Tropiiツ 100", inline=False)
            em1.add_field(name="leaderboard", value="See the leaderboard, Example: -leaderboard", inline=False)
            em1.add_field(name="slots", value="Play slots, Example: -slots", inline=False)
            em1.add_field(name="rob", value="Rob someone, Example: -rob @Tropiiツ", inline=False)
            await interaction.response.send_message(embed=em1, ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Select())

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"help"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"help"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="help", description="See staff commands or normal commands")
    @commands.check(is_enabled)
    async def help(self, ctx):
        em = discord.Embed(title="Help", description="Choose Staff Commands or Normal Commands", color=ctx.author.color)
        await ctx.send(embed=em, view=SelectView())
    

async def setup(bot):
    await bot.add_cog(help(bot))