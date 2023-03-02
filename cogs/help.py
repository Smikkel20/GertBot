import discord
import os
import random
from discord.ext.commands import Bot
from discord.ext import commands

class Helpcommand(commands.Cog):
    
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
    
    #Creates subcommand for help
    @commands.hybrid_command(name = "help", with_app_command = True, description = "Shows list of commands")
    async def help(self, ctx):
        em = discord.Embed(title = "Help", color = discord.Color.blue())
        em.add_field(name = "`;bible`", value = "gebruik `;bible` voor de link naar de Real Official Bible", inline=False)             
        em.add_field(name = "`;sw`", value = "gebruik `;sw`, `;starwars` voor starwars quotes", inline=False)
        em.add_field(name = "`;q`", value = "gebruik `;q`, `;quotes` voor official sexy quotes", inline=False)
        em.add_field(name = "`;bans`", value = "gebruik `;bans` om de bans te bekijken!", inline=False)
        await ctx.send(embed = em)

async def setup(bot):
    await bot.add_cog(Helpcommand(bot))
    print("Help has been loaded")