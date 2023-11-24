import discord, asyncio, pymongo, os
from discord.ext import commands
from dotenv import load_dotenv
from discord.ui import Button, button, View

from dotenv import load_dotenv
load_dotenv()

def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"ticket"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"ticket"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

async def send_log(title: str, guild: discord.Guild, description: str, color: discord.Color):
    log_channel = discord.utils.get(guild.channels, name="ticket-logs")
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    await log_channel.send(embed=embed)

class CreateButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Create Ticket", style=discord.ButtonStyle.blurple, emoji="🎫", custom_id="ticketopen")
    async def ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, name="OPENED TICKETS")
        for ch in category.text_channels:
            if ch.topic == f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!":
                await interaction.followup.send("You already have a ticket open! Ticket located in {0}".format(ch.mention), ephemeral=True)
                return 
            
        # make a dictionary that increases by one everytime a ticket is created
        if not category:
            category = await interaction.guild.create_category_channel("OPENED TICKETS")
            counter = 0
        else:
            counter = len(category.text_channels)

            
            
        r1: discord.Role = discord.utils.get(interaction.guild.roles, name="Ticket Master")
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await category.create_text_channel(
            # the name of the channel should be ticket- and then a counter that increases everytime a ticket is opened
            name=f"{interaction.user}-{counter + 1}",
            topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!",
            overwrites=overwrites
        )

        em = discord.Embed(description="Someone will be here to assist you shortly.\nTo close this ticket react with 🔒",color=interaction.user.color)
        em.set_footer(text="Powered by Blob", icon_url=interaction.guild.me.avatar)

        await channel.send(f"{interaction.user.mention} Welcome to your ticket. {r1.mention}\n\nPlease don't ping staff, they will be here soon.\n\n",embed=em, view=CloseButton())
        await interaction.followup.send(f"Ticket created in {channel.mention}", ephemeral=True)
        await send_log(
            title="Ticket Created",
            description=f"Created by: {interaction.user.mention}",
            color=discord.Color.green(),
            guild=interaction.guild
        )

class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="closeticket", emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send("Closing this ticket in 5 seconds")

        await asyncio.sleep(5)
        
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, name="CLOSED TICKETS")
        r1: discord.Role = discord.utils.get(interaction.guild.roles, name="Ticket Master")
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        await interaction.channel.edit(category=category, overwrites=overwrites)
        await interaction.channel.send(
            embed = discord.Embed(
                title="Ticket Closed",
                description="This ticket has been closed\n\nTicket closed by {0}".format(interaction.user.mention),
                color=interaction.user.color
            ),
            view=TrashButton()
        )
        await send_log(
            title="Ticket Closed",
            description=f"Closed by: {interaction.user.mention}",
            color=discord.Color.yellow(),
            guild=interaction.guild
        )

class TrashButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Trash Ticket", style=discord.ButtonStyle.red, custom_id="trash", emoji="🗑️")
    async def trash(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send("Deleting ticket in 3 seconds")
        await asyncio.sleep(3)

        await interaction.channel.delete()

        await send_log(
            title="Ticket Deleted",
            description=f"Deleted by: {interaction.user.mention}",
            color=discord.Color.red(),
            guild=interaction.guild
        )

class ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Tickets Online')

    @commands.hybrid_command(name="ticket", description="Create a ticket")
    @commands.has_permissions(administrator=True)
    @commands.check(is_enabled)
    async def ticket(self, ctx):
        if not discord.utils.get(ctx.guild.categories, name="OPENED TICKETS"):
            await ctx.guild.create_category(name="OPENED TICKETS")
        if not discord.utils.get(ctx.guild.categories, name="CLOSED TICKETS"):
            await ctx.guild.create_category(name="CLOSED TICKETS")
        if not discord.utils.get(ctx.guild.roles, name="Ticket Master"):
            await ctx.guild.create_role(name="Ticket Master")
        if not discord.utils.get(ctx.guild.channels, name="ticket-logs"):
            await ctx.guild.create_text_channel(name="ticket-logs")
        await ctx.send(
            embed=discord.Embed(
                description="Click the button below to create a ticket",
                color=ctx.author.color
            ),
            view=CreateButton()
        )

async def setup(bot):
    await bot.add_cog(ticket(bot))
