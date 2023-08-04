#Baseline for starting the bot
from discord.ext import commands
import discord
from discord.emt.commands import has_permissions, MissingPermissions

#importing tokens from a local file
import tokens
#alternative option
#from tokens import *



#declaring the prefixes for commands
kiroka = commands.bot(command_prefix = '!',intents = discord.Intents.all())

#welcome command to the server
@kiroka.event()
async def on_member_join(member):
    channel = client.get_channel(tokens.CHANNEL_ID)
    await channel.send("Welcome")
    
#sendoff command for when someone leaves or is booted from server
@kiroka.event
async def on_member_remove(member):
    channel = client.get_channel(tokens.CHANNEL_ID)
    await channel.send("Dont come back!")








#command for bot to join vcs
@kiroka.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("you arent in a voice channel for me to join")
        
#command for bot to leave vcs       
@kiroka.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I'm out")
    else:
        await ctx.send("i am not in a voice channel")
        
        
        
"""
Kick and ban commands

checks if the user sending the message has the ability to kick people

passes in the user thats being kicked

giving a reason as to why the user is being kicked

as well as error checking for if the user in question cant kick others
"""
@kiroka.command
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.member, *, reason = "being a stoopoo poopoohead"):
    await member.kick(reason=reason)
    await ctx.send(f"User {member} has been kicked")
    
    
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Youre to low in the hierarchy to do that lol. step up" + https://wompampsupport.azureedge.net/fetchimage?siteId=7575&v=2&jpgQuality=100&width=700&url=https%3A%2F%2Fi.ytimg.com%2Fvi%2Fl3HMALfodb8%2Fhqdefault.jpg)
        

@kiroka.command
@has_permissions(kick_members=True)
async def ban(ctx, member: discord.member, *, reason = "being a stoopoo poopoohead"):
    await member.ban(reason=reason)
    await ctx.send(f"Damn, you really wont be missed {member}")
    
    
@kick.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No" + https://media.tenor.com/vUs9lHbfbWIAAAAC/ha-ha-simpsons.gif)
        








#turning the bot on
kiroka.run(tokens.BOT_TOKEN)    