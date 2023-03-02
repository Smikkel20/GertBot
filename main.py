import os
import discord
import sys
import random
#from globalfunc import open_account, get_bank_data, skill_lvlup, lvlup, update_bank
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
from cogs.generalcmds import quotes2_reload, robert_reload
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "-", case_insensitive = True, intents=intents, owner_id = 335427967490588672)
bot.remove_command("help")

with open("txt/seks.txt", "r") as q:
    seks = []
    for line in q:
        line = line.strip()
        if line:
            seks.append(line)

load_dotenv()
#get tokens from .env file
TOKEN = os.getenv("GERT_TOKEN")

@bot.event
async def on_ready():
    print("---------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    #Sets activity 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Samson & Gert - Alles is op", url="https://open.spotify.com/track/0ovXFyO1LuOwmZkA4S2dDi?si=7761cbc4a9e7499e"))
    print('activity set')
    print('---------------')
    #get every file in ./cogs dir

@bot.event
async def setup_hook():
    print('===============')
    print("Loading Cogs")
    print('===============')
    for filename in os.listdir("./cogs"):
        #check if the filename ends with .py
        if filename.endswith(".py"):
            if not filename.startswith("__init__.py"):
                try:
                    #load <filename>
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    print(e)
                    print(f"failed to load extension {filename}", file=sys.stderr)
    print('===============')
    print("All Cogs loaded")
    print('===============')

    print('---------------')
    print("Syncing slash")
    await bot.tree.sync()
    print("Synced slash")
    print('---------------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    if isinstance(error, commands.errors.NotOwner):
        await ctx.reply(error, ephemeral = True)
    else:
        raise error

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    with open("txt/poll.txt", "r") as q:
        poll = []
        for line in q:
            line = line.strip()
            if line:
                poll.append(line)
    for msg in poll:
        if str(payload.message_id) == str(msg):
            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = bot.get_user(payload.user_id)
            if str(payload.emoji) == "<:smikkelpog:915176741868298242>" or str(payload.emoji) == "<:distressed:853371062497968128>":
                return
            if not user:
                user = await bot.fetch_user(payload.user_id)
            await message.remove_reaction(payload.emoji, user)

@bot.event
async def on_message(ctx):
    message = str(ctx.content)
    if ctx.author.bot:
        return
    await bot.process_commands(ctx)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency, 2)} ms!')

@bot.hybrid_command(name="reload", with_app_command = True, description = "Reload cogs")
@commands.is_owner()
async def reload(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            if not filename.startswith("__init__.py"):
                try:
                    #reload extensions
                    await bot.unload_extension(f"cogs.{filename[:-3]}")
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    await ctx.send(f"Reloaded {filename[:-3]}")
                except Exception as e:
                    print(f"failed to reload extension cogs.{filename[:-3]}", file=sys.stderr)




keep_alive()

try:
    bot.run(os.getenv("GERT_TOKEN"))
except:
    os.system("kill 1")