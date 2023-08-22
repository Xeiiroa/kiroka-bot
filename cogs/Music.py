import discord
from discord.ext import commands
from tokens import *

import youtube_dl
import asyncio
#? might remove
from discord import FFmpegPCMAudio
import re

#TODO create a regular expression to test youtube urls and make sure it matches whats needed


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.is_playing = False
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music is ready.")
        
    #play song
    @commands.command()
    async def play(self, ctx, url):
        
        
        if not await self.connect_to_voice(ctx):
            return
        
        self.queue.append(url)

        if self.is_playing == False:
            await ctx.send(f"Playing {url}")
            self.play_next(ctx)
        
    #skip to the next song    
    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            #! print("skipped")        
            
            if self.queue:
                self.play_next(ctx)
            else:
                self.is_playing=False
                await ctx.voice_client.disconnect()
            
        else:
            await ctx.send("nothing is playing")
            
    
    async def queue(self,ctx,url):
        if not await self.connect_to_voice(ctx):
            return
        
        self.queue.append(url)
        await ctx.send(f"{url} added to queue")
        
        #play next song if nothings playing
        if self.is_playing == False:
            await ctx.send(f"playing:{url}")
            self.play_next(ctx)
        
            
        
    #Todo depends on what is appended to the queue if this is kept or scrapped    
    @commands.command()
    async def printqueue(self, ctx):
        ...
        
        
        
    #*basic interaction events
    
    #autoleave event
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user:
            if after.channel is None:
                return
            
            if len(after.channel.members) == 1:
                await after.channel.guild.voice_client.disconnect() 
        
    #* basic functions
        
    #join vc command    
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("you are not in a voice channel")
                
    
    #leave vc command
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        if (ctx.voice_client):
            if self.is_playing:
                self.is_playing = False
            
            await ctx.guild.voice_client.disconnect()
            
        else:
            await ctx.send("I'm not in a voice channel.")
                
    
    
    
    #* utility functions
    
    
    #check if the author is in a vc and if they are join it, if not send false
    async def connect_to_voice(self, ctx):
        #if author isnt in a vc at all
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("you need to be in a vc to use this command")
            return False
        
        #if bot is not in a vc but author is
        if ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
            
        return True
     
    #TODO find actual docs to go more in depth and understand how to do  
    #play next song
    def play_next(self,ctx):
        if self.queue:
            #? pop(0)
            url = self.queue.pop(0)
            self.is_playing = True
            
            #?
            #TODO add actual playing for yt and spotify
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    url2 = info['entries'][0]['url']
                else:
                    url2 = info['formats'][0]['url']

            voice_client = ctx.voice_client
            voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: self.after_play(ctx))

        else:
            self.is_playing = False
            
        
    
    #checks if the queue is empty or not and if not plays the next song    
    def after_play(self,ctx):
        if not self.queue:
            self.is_playing = False
            #?
            asyncio.run_coroutine_threadsafe(ctx.voice_client.disconnect(), self.bot.loop)
        
        else:
            self.play_next(ctx)
    

        
async def setup(client):
    await client.add_cog(Music(client))