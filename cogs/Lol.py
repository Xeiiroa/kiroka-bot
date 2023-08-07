import discord
from discord.ext import commands
from tokens import *

class Lol(commands.Cog):
    def __init__(self, client):
        self.client = client
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Lol is ready.")
        
        
async def setup(client):
    await client.add_cog(Lol(client))