import discord
from discord.ext import commands

class ExceptionHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please pass in all required arguments.")
        if isinstance(error, commands.MissingRole):
            await ctx.send("You do not have the role required to use this command.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions to run this command.")
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Sorry, but that command doesn't exist. Please use `-help` to find commands")
        if isinstance(error, commands.BotMissingRole):
            await ctx.send("The bot doesnt have the required role to use this command.")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("The bot is missing the required permissions to use this command.")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("There is something wrong with the code please ask Tropiiツ#0001 and ask him to fix the issue.")
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("You are missing the role to run this command please make sure you have the role and try again")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown please wait {round(error.retry_after * 1)} seconds before using it again")
        if isinstance(error, commands.CheckFailure):
            await ctx.send("This command has been disabled in your server.")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExceptionHandler(bot))