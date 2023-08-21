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
    
    
    
        
    
        
        
async def setup(client):
    await client.add_cog(Basics(client))
        
    
    
    
    
    
    
