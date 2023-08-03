#Baseline for starting the bot
from discord.ext import commands
import discord

#importing tokens from a local file
import tokens
#alternative option
#from tokens import *

#declaring the prefixes for commands
kiroka = commands.bot(command_prefix = '!')
    
    




#turning the bot on
kiroka.run(tokens.BOT_TOKEN)    