import discord
from discord.ext import commands
import os

#import tokens
from tokens import *


#declaring the prefixes for commands
bot = commands.Bot(command_prefix = '!',intents = discord.Intents.all())

#bot ready message
@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Bot is ready")
 
#create a list to hold filenames that need to be imported    
initial_extensions =[]    

#iterate over the cogs file and if the file ends with .py appends it to our list while removing ".py" from said file
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initial_extensions.append("cogs." + filename[:-3])
        
        
if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)
    
 
#turning on bot    
bot.run(BOT_TOKEN)