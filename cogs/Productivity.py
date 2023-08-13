import discord
from discord.ext import commands
from tokens import *

#for study sessions
import datetime
from dataclasses import dataclass


class Productivity(commands.Cog):
    def __init__(self, client):
        self.client = client
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Productivity is ready.")
    
    
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
        
            
        
        
async def setup(client):
    await client.add_cog(Productivity(client))