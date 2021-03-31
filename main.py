import os
import discord
import random
import praw
import sys
import validators
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color
from dotenv import load_dotenv
from keep_alive import keep_alive

bot = commands.Bot(command_prefix = "!")
bot.remove_command("help")

if __name__ == "__main__":
    #get every file in ./cogs dir
    for filename in os.listdir("./cogs"):
        #check if the filename ends with .py
        if filename.endswith(".py"):
            try:
                #load <filename>
                bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"failed to load extension {filename}", file=sys.stderr)

load_dotenv()
#get tokens from .env file
TOKEN = os.getenv("TEST_TOKEN")
RedditPassword = os.getenv("REDDIT_PASSWORD")

@bot.event
async def on_ready():
    print("---------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    #Sets activity 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="twitch.tv/JunJiRah"))
    print('activity set')
    print('---------------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    else:
        raise error

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {bot.latency} ms!')

@bot.command()
async def reload(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                #reload extensions
                bot.unload_extension(f"cogs.{filename[:-3]}")
                bot.load_extension(f"cogs.{filename[:-3]}")
                await ctx.send(f"Reloaded {filename[:-3]}")
            except Exception as e:
                print(f"failed to reload extension cogs.{filename[:-3]}", file=sys.stderr)




keep_alive()
bot.run(TOKEN)
