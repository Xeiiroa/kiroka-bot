import discord
from discord.ext import commands
from tokens import *
import random
from pixivapi import Client





class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Client()
        self.client.login(PIXIV_USERNAME, PIXIV_PASSWORD)
     
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
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello kind stranger!")
            
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
    
    @commands.commad()
    async def pixiv(self, ctx, keyword):
        ...
    
            
        
    
        
        
    
                
    
        
        
async def setup(bot):
    await bot.add_cog(Chat(bot))