import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from typing import Any, Literal, Optional, Type
import os
import asyncio

"""from discord.ext.commands.bot import PrefixType, _default
from discord.ext.commands.help import HelpCommand"""

#import tokens
from tokens import *

#sync command
#loading 

class Oyasu(commands.Bot):
    def __init__(self, intents: discord.Intents=discord.Intents.all(), activity=discord.Game(name="リグマ")):
        super().__init__(command_prefix="!", intents=intents, activity=activity, help_command=None)
        
        #self.change_presence(status=discord.Status.online, activity=discord.Game(name="リグマ"))
    
    
    async def setup_hook(self) -> None:
        await self.load()
        #!remove after testing
        #await self.tree.sync()
        
        
        
        
    async def load(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
               
            

async def main():
    async with Oyasu() as bot:
        #bot.remove_command('help')
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())



    
    
    
"""async with Oyasu as bot:
        await bot.remove_command('help')
        await bot.start(BOT_TOKEN)
"""

"""def main():
    bot = Oyasu()
    bot.remove_command('help')
    bot.start(BOT_TOKEN)
        """