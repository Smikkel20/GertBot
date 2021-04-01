import os
import discord
import sys
import datetime, time
import json
import threading
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

def LastTime():
    while True:
        #get current time
        LastKnownTime = time.time()
        #store the current time in time.json
        try:
            time_file = open("time.json", "r")
            json_object = json.load(time_file)
            time_file.close()
            json_object["time"] = LastKnownTime
            time_file = open("time.json", "w")
            json.dump(json_object, time_file)
            time_file.close()
        #if the file is empty create the object
        except json.JSONDecodeError:
            time_file = open("time.json", "w")
            time_file.write('{"time" : ')
            time_file.write(str(LastKnownTime))
            time_file.write("}")
            

@bot.event
async def on_ready():
    print("---------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

    #Sets activity 
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="twitch.tv/JunJiRah"))
    #print('activity set')
    
    #starts LastTime loop
    b.start()
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
async def uptime(ctx):
        #get current time
        current_time = time.time()

        #get the amount of seconds between time the script started and current time
        difference = int(round(current_time - start_time))
        #get the amount of seconds between the last known time of the last time the script has run and start time
        down_time_difference = int(round(start_time - last_down_time))
        
        #convert it to  hh:mm:ss format
        text = str(datetime.timedelta(seconds=difference))
        text2 = str(datetime.timedelta(seconds=down_time_difference))

        #last time the script was down in local time
        down_time = time.asctime(time.localtime(start_time))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.add_field(name="Uptime", value=text)
        embed.add_field(name="Last Downtime", value=f"at {down_time} for {text2}")
        embed.set_footer(text=bot.user.name)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

@bot.command()
async def reload(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                #reload extensions
                bot.unload_extension(f"cogs.{filename[:-3]}")
                bot.load_extension(f"cogs.{filename[:-3]}")
                await ctx.send(f"Reloaded {filename[:-3]}")
            except Exception:
                print(f"failed to reload extension cogs.{filename[:-3]}", file=sys.stderr)

#creates a multitread for the 
b = threading.Thread(name='LastTime', target=LastTime)

time_file = open("time.json", "w")
time_file.close()

#get the last known uptime time from time.json
try:
    time_file = open("time.json", "r")
    json_object = json.load(time_file)
    time_file.close()
    print(json_object["time"])
    last_down_time = json_object["time"]
except json.JSONDecodeError:
    print("An exception occured while trying to read time.json returning current time")
    last_down_time = time.time()

#retrieve the time from when the bot starts
start_time = time.time()

#activates the webserver
keep_alive()

bot.run(TOKEN)
