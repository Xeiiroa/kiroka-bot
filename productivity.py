import discord
from discord.ext import commands
from tokens import *

#for study sessions
import datetime, time
from dataclasses import dataclass

"""
session start(task, max time, maxtime units: default=Minutes, break time)
params
task: self explanatory
break time(sends a reminder to take a break at intervals of that time)
maxtime: how long a session for a task will last until it auto ends
maxtime units(the time you want the session in hours or minutes)
___


async def send_break_message(time)
goal
once a a time interval is crossed activate this command and send a message
reminding the author to take a break 

and after a given amount of time repeat 15-20 min


session_end()
ends session   
    
    
    
"""
#TODO 
#turn all these commands into hybrid commands
class Productivity(commands.Cog):
    def __init__(self, client):
        self.client = client
        #? This is a dict for checking if the user has a session going and if not remove them from the list
        session_userbase={}
        #? This is a dict that will add the users id to it and add a list with multiple keys for each task
        task_userbase={}
        #session would hold a list for guild members and check if that person has a session
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Productivity is ready.")
        
    #! error check so i dont forget
    #if breaktime is longer than maxtime return error    
    
    #?@commands.hybrid_command(name="session start", description="Starts a session for you to focus on a task w breaks.")
    @commands.describe(maxtime='The maximum duration(in minutes) of the task session before it automatically ends')
    @commands.describe(task='The reason you want to start the session')
    @commands.describe(breaktime='time between Oyasu reminding you to take a break(in minutes)')
    async def sessionstart(self, ctx, task="Study", maxtime=0, breaktime=0):
        ...
     
    #at the end of the timer call sessionend
     
     
    #    
    async def session_end(self, ctx, task):
        ...
        
    async def remindme(self, ctx, thing):
        """
        Grab user id 
        check if said id is in the dict 
        if it is then add that thing to the list of reminders
            if not then add their id to the list as well as a list for their value and add the task
        """
    
    async def reminders(self, ctx):
        """
        Check user id
        Check their list of reminders if there are any
          if their is create an embed W a list of the things that they have using a for loop and '\n'.join
            if not say they dont got nun
        """
    async def undermindme(self, ctx, thing):
        """
        Check user id 
        if theyre in the dict then remove the given task from the list and tell them u did it
        
        if that item isnt in their list then tell them what is
        
        and if they aren in the dict tell them
        """
        
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
        
            
        
        
"""async def setup(client):
    await client.add_cog(Productivity(client))"""