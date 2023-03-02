import discord
import os
import youtube_dl
import validators
import re
import urllib
from discord.ext.commands import Bot
from discord.ext import commands

def searchurl(url):
    if not validators.url(url) == True:
        query_string = urllib.parse.urlencode({
            'search_query': url
        })
        print(query_string)
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_content= htm_content.read().decode()
        url = re.findall(r'\/watch\?v=\w+', search_content)
        url = f"https://www.youtube.com{url[0]}"
        print(url)
        return url

class Musiccommand(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot


    @commands.command()
    async def play(self, ctx, *url):
        print(url)
        url = str(url)
        url = url.replace(" ","+")
        print(url)
        url = url[2:-2]
        print(url)
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            if not validators.url(url) == True:
                url = searchurl(url)
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return
        #Check if user is in vc
        voice_state = ctx.author.voice
        if voice_state is None:
            return await ctx.send('You need to be in a voice channel to use this command')
        #get the user his channel and the voice_client of the guild
        channel = ctx.author.voice.channel
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        #check that the bot isnt already connected to a vc in that guild
        if not voice_client == None:
            #check if the bot isnt connected to a your vc
            if not channel == voice_client.channel:
                return await ctx.send('im already connected to another vc')
        else:
            await channel.connect()
        if not validators.url(url) == True:
            url = searchurl(url)
        print(url)
        #get the voice again after connection
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
    
    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")


    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")


    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.stop()

    @commands.command()
    async def replay(self, ctx):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        try:
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
        except Exception:
            await ctx.send("Couldnt find last song")
        



async def setup(bot):
    await bot.add_cog(Musiccommand(bot))
    print("Music has been loaded")