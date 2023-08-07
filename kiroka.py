import discord
from discord.ext import commands
import os
import asyncio

#import tokens
from tokens import *


#declaring the prefixes for commands
client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

#bot ready message
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="リグマ"))
    print("bot ready \n --------------------------")
 
        
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename[:-3]} imported")
            
async def bot_start():
    async with client:
        await load()
        await client.start(BOT_TOKEN)
        
asyncio.run(bot_start())
            
        
        
        
