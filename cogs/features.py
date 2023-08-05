#this file holds all our general commands that dont belong in a specific main category

import discord
from discord.ext import commands
from tokens import *

class features(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    class Anime():
        ...
    
    class Productivity():
        ...
    
    class Music():
        ...
    
    class osu():
        ...
    
    class lol():
        ...
    
    class val():
        ...
        
    class etc():
        ...
        
    

def setup(bot):
    bot.add_cog(features(bot))