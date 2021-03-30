import discord
import os
import random
from discord.ext.commands import Bot
from discord.ext import commands

class Gamercommand(commands.Cog):
    
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def gamer(self, ctx, user : discord.Member):
        Elite = random.randint(1,10)
        print(Elite)
        GamerEmbed = discord.Embed(
            title = f"Is {user.name} an Elite Gamer?",
            color = user.color
        )
        if Elite == 1:
            GamerEmbed.description = f"{user.name} is an elite gamer"
            GamerEmbed.set_image(url="https://cdn.frankerfacez.com/emoticon/210748/1")
        else:
            GamerEmbed.description = f"{user.name} is NOT an elite gamer"
            GamerEmbed.set_image(url="https://cdn.frankerfacez.com/emoticon/381875/1")
        await ctx.send(embed=GamerEmbed)

    @gamer.error
    async def gamer_error(self, ctx ,error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            Elite = random.randint(1,10)
            print(Elite)
            GamerEmbed = discord.Embed(
                title = f"Is {ctx.author.name} an Elite Gamer?",
                color = ctx.author.color
            )
            if Elite == 1:
                GamerEmbed.description = f"{ctx.author.name} is an elite gamer"
                GamerEmbed.set_image(url="https://cdn.frankerfacez.com/emoticon/210748/1")
            else:
                GamerEmbed.description = f"{ctx.author.name} is NOT an elite gamer"
                GamerEmbed.set_image(url="https://cdn.frankerfacez.com/emoticon/381875/1")
            await ctx.send(embed=GamerEmbed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Gamercommand(bot))
    print("Gamer has been loaded")