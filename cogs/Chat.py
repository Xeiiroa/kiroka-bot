import discord
from discord.ext import commands
from tokens import *
import random

class Chat(commands.Cog):
    def __init__(self, client):
        self.client = client
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Chat is ready.")
        
        
        
    @commands.command()
    async def roll(self , ctx, die=1):
        for i in range(die):
            x = random.randint(1, 6)
            if die > 1:
                ctx.send(f"you rolled {x} for die {i}")
            else:
                ctx.send(f"you rolled {x}")
                
    
        
        
async def setup(client):
    await client.add_cog(Chat(client))