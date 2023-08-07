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
        
        
async def setup(client):
    await client.add_cog(Productivity(client))