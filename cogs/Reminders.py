import discord
from discord.ext import commands, tasks
from tokens import *

#for study sessions
import datetime
from dataclasses import dataclass

#! IMPORTANT:
#! these commands will not be active until i finish fully grasping an understanding on sql
#! a database is required to allow things like these to scale

class Reminders(commands.Cog):
    def __init__(self, client):
        self.client = client
     
    
        
            
        
        
async def setup(client):
    await client.add_cog(Reminders(client))