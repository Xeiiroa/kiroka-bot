#this file holds all our general commands that dont belong in a specific main category

import discord
from discord.ext import commands
from tokens import *
import datetime
from dataclasses import dataclass


class features(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          
          
    #anime related functions        
    class Anime():
        ...
    
    
    #productivity
    class Productivity():
        # function for if you need to set time to focus on a task
        
        @dataclass
        class Session:
            
            session_active: bool = False
            start_time: int = 0
            
            @commands.command
            async def taskstart(cls, ctx, task):
                if session_active == True:
                    await ctx.send(f"another session has already been started")
                    return
                
                session_active = True
                start_time = ctx.message.created_at.timestamp()
                normaltime = ctx.message.created_at.strftime("%H:%M")
                await ctx.send(f"Session for {task} started at {normaltime}")
                
            @commands.command
            async def taskend(cls, ctx):
                if session_active == False:
                    await ctx.send("There isnt a session for me to end")
                    return
                
                session_active = False
                end_time = ctx.message.created_at.timestamp()
                normalduration = str(datetime.timedelta(seconds=duration))
                duration = end_time - cls.start_time
                await ctx.send(f"Session ended after {normalduration}")
                
            
            
        
        
    
    class Music():
        ...
    
    class osu():
        ...
    
    class lol():
        ...
    
    class val():
        ...
        
    class etc():
        ...
        
    

def setup(bot):
    bot.add_cog(features(bot))