

#! update
"""
as of this moment to my knowledge and searching i am to believe that there isnt a physical way
for discord bots to play music using discord.py 

the only bot i have found that could was make in java 
so ill be scrapping this jumbled set and pursue other features for interraction
"""
    
    














import discord
from discord.ext import commands
from tokens import *

import youtube_dl
import asyncio
from discord import FFmpegPCMAudio
import re


class GuildMusicState:
    def __init__(self):
        self.song_queue = []
        self.is_playing = False
        self.voice_channel = None
    #todo impliment autoplay
   #todo create error check if bot not in voice do for all commands 
   #todo also create a parameteer to check if the bot is in voice and if they arent to change statuses(for if user kicks bot)
    #itd be before the error checks
    #todo IMPORTANT
    #! when you are out of trackss automatically set it so that it turns off isplaying for that guild
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        #? should hold and be a checking point for guild status
        self.guld_music_states = {}
     
    #* ready command to make sure it still imports   
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music is ready.")
        
        
        #!whhy did i [put utrl in play next and how can i do it with safe cehck foir with adn without url]
    #play song
    @commands.command()
    async def play(self, ctx, url):
        #todo if the user is in a vc join it else print error
        
        audio_url = await self.get_audio_url(url)
        # check for if there is a queue already and if there is override it and play desired track
        if self.song_queue:
            self.guild_music_states[ctx.guild_id].queue.insert(0, audio_url)
            await ctx.send(f"Playing {url}")
            await self.play_next(ctx)
        
            
        elif not self.guild_music_states[ctx.guild.id].is_playing and audio_url:
            self.guild_music_states[ctx.guild.id].is_playing = True
            await ctx.send(f"Playing {url}")
            await self.play_next(ctx) 
        
        
        #! assuming there is no queue playing should be false
        elif audio_url:
            await self.queue(ctx, url)     
           
        
        

    #skip to the next song    
    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            self.play_next(ctx)
        
        
            
    #adds a new song to the queue
    @commands.command()
    async def queue(self,ctx,url):
        audio_url = await self.get_audio_url(url)
        
        if audio_url:
            self.guild_music_states[ctx.guild_id].queue.append(audio_url)
            await ctx.send(f"Added {url} to the queue.")
        
            if not self.guild_music_states[ctx.guild_id].is_playing:
                    self.guild_music_states[ctx.guild_id].is_playing = True
                    await self.play_next(ctx)   
        else:
            await ctx.send("Invald url provided")    
            
    
    
    

    @commands.command()
    async def printqueue(self,ctx):
        ...           
               
    
    #* utility functions
    
    #check if the author is in a vc and if they are join it, if not send false
    async def connect_to_voice(self, ctx):
       ...
       
       
    #make sure its a proper youtube audio and return the import
    async def get_audio_url(self, url):
        if link := re.search(r"^((https?://(?:www\.)?(?:m\.)?youtube\.com))/((?:oembed\?url=https?%3A//(?:www\.)youtube.com/watch\?(?:v%3D)(?P<video_id_1>[\w\-]{10,20})&format=json)|(?:attribution_link\?a=.*watch(?:%3Fv%3D|%3Fv%3D)(?P<video_id_2>[\w\-]{10,20}))(?:%26feature.*))|(https?:)?(\/\/)?((www\.|m\.)?youtube(-nocookie)?\.com\/((watch)?\?(app=desktop&)?(feature=\w*&)?v=|embed\/|v\/|e\/)|youtu\.be\/)(?P<video_id_3>[\w\-]{10,20})", url, re.IGNORECASE):
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
            return info['formats'][0]['url']
        
    
    

    """
    check if the server has a queue going 
    and if they do play the next song and remove the last song from the list
    """
    #play next song
    def play_next(self,ctx, url):
        audio_url = self.get_audio_url(url)
        
        if audio_url:
            #!check
            voice_state = self.guild_music_states[ctx.guild_id]
            if voice_state.queue:
                next_url = voice_state.queue.pop(0)
                voice_client = voice_state.voice_channel.guild.voice_client
                voice_client.play(discord.FFmpegPCMAudio(next_url), after=lambda e: self.after_play(ctx))
            else:
                voice_state.playing = False
        
            
            
    #checks if the queue is empty or not and if not plays the next song    
    def after_play(self,ctx):
        voice_state = self.guild_music_states[ctx.guild_id]
        voice_client = voice_state.voice_channel.guild.voice_client
        if voice_client.is_playing():
            return
        if voice_state.song_queue:
            self.play_next(ctx)
        
        
    #*basic interaction events
    
    #todo add functionality so that when each of these are called they clear the queue
    
    #autoleave event
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user:
            if after.channel is None:
                return
            
            if len(after.channel.members) == 1:
                await after.channel.guild.voice_client.disconnect() 
        
        
    #join vc command    
    @commands.command()
    async def join(self, ctx):
        ...
                
    
    #leave vc command
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        if (ctx.voice_client):
            if self.is_playing:
                self.is_playing = False
            
            await ctx.guild.voice_client.disconnect()
            
        else:
            await ctx.send("I'm not in a voice channel.")
    

        
async def setup(client):
    await client.add_cog(Music(client))