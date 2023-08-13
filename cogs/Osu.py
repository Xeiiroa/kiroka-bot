import discord
from discord.ext import commands
from tokens import *
import requests
import json

from ossapi import Ossapi

class Osu(commands.Cog):
    def __init__(self, client):
        self.client = client
        api = Ossapi(OSU_CLIENT_ID, OSU_SECRET)
        
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Osu is ready.")
        
        
    api = Ossapi(client_id, client_secret)
        
        
        
        
        
async def setup(client):
    await client.add_cog(Osu(client))