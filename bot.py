from commands import help, ticket

# pip install imports
import discord, aiofiles
from discord.ext import commands

from dotenv import load_dotenv
import asyncio 
import pymongo

# sys imports
import os 
import logging
import logging.handlers

load_dotenv()

import sentry_sdk
sentry_sdk.init(
    dsn=os.getenv("key"),

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

def get_server_prefix(bot, message):
    client = pymongo.MongoClient(os.getenv("mongo_url"))
    db = client.servers
    coll = db.prefixes

    if coll.find_one({"_id":message.guild.id}):
        prefix = coll.find_one({"_id":message.guild.id})["prefix"]
        return prefix

# startup stuff
load_dotenv()

intents = discord.Intents().default()
intents.message_content = True
intents.guilds = True
intents.members = True

# create the bot
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_server_prefix, intents = intents)
        self.synced = False
        self.warnings = {}
        self.remove_command("help")     
        
    async def setup_hook(self):
        self.add_view(help.SelectView())
        self.add_view(ticket.CreateButton())
        self.add_view(ticket.CloseButton())
        self.add_view(ticket.TrashButton())
        print(f'\33[32mLogged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def load_extensions(self):
        for name in os.listdir('./commands'):
            if name.endswith('.py'):
                await self.load_extension(f'commands.{name[:-3]}')

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(self.guilds)} servers!"))

        for guild in self.guilds:
            # find the channel named "commands"
            owner = guild.owner
            await owner.send("Hello Again!\n\nThis is an official message from the developer of Blob. We are continuing development of Blob and it will resume normal operations shortly.\n\nA lot has changed since the last time Blob was online. We are here to address your issues with our new discord server. Please join [now](https://discord.gg/A2EQDvA6sN).\n\nI (Tropii) hate to send messages to server owners like you with stuff like this, I do apologize. For further information please join the support server below!\n\nTake care - Tropii.\n\nHave any conerns? Feel free to add me `fstropii`\n\nIf you see this message more than once please let me know ASAP!")

# making var for commands in this file
bot = MyBot()

# start bot
async def main():
    async with bot:
        await bot.load_extensions()
        await bot.start(os.getenv("token"))
        await asyncio.sleep(0.1)
    await asyncio.sleep(0.1)

asyncio.run(main())
