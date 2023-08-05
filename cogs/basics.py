import discord
from discord.ext import commands
from tokens import *
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
import requests
import json
import os

#this class contains all basic default functions
class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    #Hello command 
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello kind stranger!")
        
    #user join event
    @commands.Cog.listener()
    async def on_member_join(member):
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("Welcome to da server")
        
    #user leave event
    @commands.Cog.listener()
    async def on_member_remove(member):
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("Dont come back!")
        
    #command for bot to join vcs
    @commands.command(pass_context = True)
    async def join(ctx):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("you arent in a voice channel for me to join")
            
    #command for bot to leave vcs       
    @commands.command(pass_context = True)
    async def leave(ctx):
        if (ctx.voice_bot):
            await ctx.guild.voice_bot.disconnect()
            await ctx.send("I'm out")
        else:
            await ctx.send("i am not in a voice channel")
        
            
            
    
def setup(bot):
    bot.add_cog(Basics(bot))