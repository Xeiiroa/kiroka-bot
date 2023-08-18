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
        
        
    #roll a die or multiple     
    @commands.command()
    async def roll(self , ctx, die=1):
        for i in range(die):
            x = random.randint(1, 6)
            if die > 1:
                await ctx.send(f"you rolled {x} for die {i}")
            else:
                await ctx.send(f"you rolled {x}")
                
    #pick a number between x and y            
    @commands.command()
    async def between(self, ctx, x = 0, y = 10):
        z = random.randint(x, y)
        await ctx.send(z)
        
        
    #flip a coin
    @commands.command()
    async def flip(self , ctx):
        result = random.randint(1,2)
        if result == 1:
            await ctx.send("Heads.")
        else:
            await ctx.send("Tails.")
    
    #choose between 2 choices
    @commands.command()
    async def choose(self, ctx, choicea="choice A", choiceb ="choice B"):
        x = random.randint(1,2)
        if x == 1:
            await ctx.send(f"{choicea} wins!")
        else:
            await ctx.send(f"{choiceb} wins!")
    
    
            
        
    
        
        
    
                
    
        
        
async def setup(client):
    await client.add_cog(Chat(client))