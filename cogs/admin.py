import discord
from discord.ext import commands
from tokens import *

#this class contains all basic default functions
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    """
    Kick and ban commands

    checks if the user sending the message has the ability to kick people

    passes in the user thats being kicked

    giving a reason as to why the user is being kicked

    as well as error checking for if the user in question cant kick others
    """
    @commands.command
    @has_permissions(kick_members=True)
    async def kick(ctx, member: discord.member, *, reason = None):
        await member.kick(reason=reason)
        await ctx.send(f"User {member} has been kicked")
        
        
    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Youre to low in the hierarchy to do that lol. step up" + https://wompampsupport.azureedge.net/fetchimage?siteId=7575&v=2&jpgQuality=100&width=700&url=https%3A%2F%2Fi.ytimg.com%2Fvi%2Fl3HMALfodb8%2Fhqdefault.jpg)
            

    @commands.command
    @has_permissions(kick_members=True)
    async def ban(ctx, member: discord.member, *, reason = None):
        await member.ban(reason=reason)
        await ctx.send(f"Damn, you really wont be missed {member}")
        
        
    @kick.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No" + https://media.tenor.com/vUs9lHbfbWIAAAAC/ha-ha-simpsons.gif)

            
            
    
def setup(bot):
    bot.add_cog(Admin(bot))