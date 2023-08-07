import discord
from discord.ext import commands
from tokens import *
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
import requests
import json
import os




class Basics(commands.Cog):
    def __init__(self, client):
        self.client = client
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Basics is ready.") 
    
    
    #Hello command
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello kind stranger!")
        
    #join vc command    
    @commands.command(pass_context = True)
    async def join(self, ctx):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect
            
    #leave vc command
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I'm out.")
        else:
            await ctx.send("I'm not in a voice channel.")
            
        
        
async def setup(client):
    await client.add_cog(Basics(client))
        
    
    
    
    
    
    
"""

bot had errors where client was unable to be read however they have little use to me so i may revisit them later maybe not
        
        #user join event
    @commands.Cog.listener()
    async def on_member_join(member):
        channel = client.get_channel(CHANNEL_ID)
        await channel.send("Welcome to da server")
        
    #user leave event
    @commands.Cog.listener()
    async def on_member_remove(member):
        channel = client.get_channel(CHANNEL_ID)
        await channel.send("Dont come back!")
        
        
        
"""