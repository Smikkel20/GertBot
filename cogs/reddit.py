import os
import discord
import random
import praw
import validators
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color
from dotenv import load_dotenv

#grave `

load_dotenv()

RedditPassword = os.getenv("REDDIT_PASSWORD")

#reddit bot application
Reddit = praw.Reddit(
    client_id = "yUXUyOL1oszbGw",
    client_secret = "IwNFyG01TVRQOUPHdabfZ46i8EjoeQ",
    username = "Smikkel20",
    password = RedditPassword,
    user_agent = "Agent123",
    check_for_async = False
)

class Redditcommand(commands.Cog):
    
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
    
    @commands.command()
    async def reddit(self, ctx ,sub = "memes" , description = ""):
        if validators.url(sub) == True:
            #check if its a reddit link
            if not "reddit" in sub:
                await ctx.send("That is not a reddit link!")
            #get the submission id from the link
            url = sub
            idx = url.find('comments')
            sub = url[idx+9:idx+15]
            #fetch the submission and subreddit
            sub = Reddit.submission(sub)
            subreddit = sub.subreddit
            #check if the submission or subreddit is NSFW
            if subreddit.over18 and not ctx.channel.is_nsfw() or sub.over_18 and not ctx.channel.is_nsfw():
                await ctx.message.delete()
                await ctx.send("This channel is not NSFW!")
                return
            #get the title, url, link and upvotes of the submission
            name = sub.title
            url = sub.url
            upvotes = ":arrow_up: "+str(sub.score)
            link = "https://reddit.com"+sub.permalink
            #create an embed
            MemeEmbed = discord.Embed(title = name, url = link, description = upvotes, color = ctx.author.color)
            MemeEmbed.set_image(url = url)

            await ctx.send(embed=MemeEmbed)
            return
        #check if the link was written wrong
        elif ".com" in sub:
            if not sub == "reddit.com":
                MemeEmbed = discord.Embed(title = "Thats not a valid link", description = '`https://reddit.com/r/<subreddit>/comments/<id>/<title>`', color = ctx.author.color)
                await ctx.send(embed=MemeEmbed)
                return


        #get the subreddit and top 50 submissions
        subreddit = Reddit.subreddit(sub)
        #check if the subreddit is NSFW
        if subreddit.over18 and not ctx.channel.is_nsfw():
            await ctx.send("This channel is not NSFW!")
            return

        #get the top submission from the last 24 hours
        top = subreddit.top(time_filter = "day")
        
        #all submissions
        all_subs = []

        #rotate through all submission
        for submission in top:
            all_subs.append(submission)
            
        #choose a random top submission of today
        random_sub = random.choice(all_subs)
        print(random_sub)
            
        #get the title, url, link and upvotes of the submission
        name = random_sub.title
        url = random_sub.url
        upvotes = ":arrow_up: "+str(random_sub.score)
        link = "https://reddit.com"+random_sub.permalink

        #create an embed
        MemeEmbed = discord.Embed(title = name, url = link, description = upvotes, color = ctx.author.color)
        MemeEmbed.set_image(url = url)

        await ctx.send(embed=MemeEmbed)

#do this when reddit gets loaded
def setup(bot):
    bot.add_cog(Redditcommand(bot))
    print("Reddit has been loaded")