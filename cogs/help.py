import discord
import os
import random
from discord.ext.commands import Bot
from discord.ext import commands

class Helpcommand(commands.Cog):
    
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
    
    #Creates subcommand for help
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title = "Help",description = "Use `!help <command>` for information about the command",color = ctx.author.color)

        await ctx.send(embed = em)

    @help.command()
    async def ping(self, ctx):
        em = discord.Embed(title = "Ping",description = "Shows how much ms the message took to get to you!",color = ctx.author.color)

        em.add_field(name = "**Syntax**", value = "`!ping`")

        await ctx.send(embed = em)

    @help.command()
    async def gamer(self, ctx):
        em = discord.Embed(title = "Gamer",description = "Are you an elite gamer?",color = ctx.author.color)

        em.add_field(name = "**Syntax**", value = "`!gamer`")

        await ctx.send(embed = em)

    @help.command() 
    async def reddit(self, ctx):
        em = discord.Embed(title = "Reddit",description = "Shows you a random top submission from a subreddit.",color = ctx.author.color)

        em.add_field(name = "**Syntax**", value = "`!reddit <subreddit>` or `!reddit <url>`")

        await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(Helpcommand(bot))
    print("Help has been loaded")