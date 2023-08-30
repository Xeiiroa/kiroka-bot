import discord
from discord.ext import commands
from tokens import *
import random
import requests
from pixivapi import Client





class Chat(commands.Cog):
    def __init__(self, client):
        
        self.client = client
        #self.client.login(PIXIV_USERNAME, PIXIV_PASSWORD)
     
    #Ready event    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Chat is ready.")
        
    #bot join message
    @commands.Cog.listener()
    async def on_guild_join(guild):
        welcome_channel = guild.system_channel
        
        if welcome_channel is not None:
            await welcome_channel.send(f"Thanks for having me")
           
    
    #Hello command
    @commands.hybrid_command(name="hello", description="Say hi to Oyasu")
    async def hello(self, ctx):
        await ctx.send("<:Silver:1146489422905356368>")
        await ctx.send("Hello kind stranger!")
        
            
    #roll a die or multiple     
    @commands.hybrid_command(name="roll", description="roll a given number of die")
    async def roll(self , ctx, die_number=1):
        if die_number > 1:
            rolls = "you rolled"
            for i in range(die_number):
                if i == 1:
                    x = random.randint(1, 6)
                    rolls += f" {x}"
                else:   
                    x = random.randint(1, 6)
                    rolls += f", {x}"
                    
                    await ctx.send(rolls)
        else:
            x = random.randint(1, 6)
            await ctx.send(f"you rolled {x}")
                
    
    #pick a number between x and y            
    @commands.hybrid_command(name="between", description="Oyasu picks a number between the 2 numbers you provide")
    async def between(self, ctx, x = 0, y = 10):
        z = random.randint(x, y)
        await ctx.send(z)
        
        
    #flip a coin
    @commands.hybrid_command(name="flip", description="Oyasu flips a coin")
    async def flip(self , ctx):
        result = random.randint(1,2)
        if result == 1:
            await ctx.send("Heads.")
        else:
            await ctx.send("Tails.")
    
    #choose between 2 choices
    @commands.hybrid_command(name="choose", description="Oyasu chooses between 2 options for you")
    async def choose(self, ctx, choicea="choice A", choiceb ="choice B"):
        x = random.randint(1,2)
        if x == 1:
            await ctx.send(f"{choicea} wins!")
        else:
            await ctx.send(f"{choiceb} wins!")
    

        
async def setup(client):
    await client.add_cog(Chat(client))