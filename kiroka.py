import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from typing import Literal, Optional
import os
import asyncio

#import tokens
from tokens import *


#declaring the prefixes for commands
client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

#command sync command
#TODO make sure that the sync command is only usable in oyasus server and only by me

@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.client.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.client.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.client.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.client.tree.clear_commands(guild=ctx.guild)
            await ctx.client.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.client.tree.sync()
        
        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


#bot ready message
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="リグマ"))
    #! REMOVE AFTER TESTING PHASE YOU ALREADY HAVE A SYNC COMMAND
    await client.tree.sync()
    print("bot ready \n --------------------------")
 
        
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            
            
async def bot_start():
    async with client:
        await load()
        await client.start(BOT_TOKEN)
        
asyncio.run(bot_start())
            
        
        
        
