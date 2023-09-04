#* Owner only commands
import discord
from discord import app_commands
from discord.ext import commands, Greedy, Context
from tokens import *
from typing import Any, Literal, Optional, Type


import os
import asyncio

from discord.ext.commands.bot import PrefixType, _default
from discord.ext.commands.help import HelpCommand

#import tokens
from tokens import *


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
        

async def setup(bot):
    await bot.add_cog(Owner(bot))